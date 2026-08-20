#   TriChord - Firefox extension API generator
#   -------------------------------
#
#   Adapted from Domato (Ivan Fratric, Google Project Zero).
#   Generates Firefox WebExtensions test cases (browser.* Promise-style APIs).
#   Supports --subsystem <name> to focus generation on a single subsystem
#   (e.g. tabs, windows, bookmarks, browsingData, contextMenus, runtime ...).

from __future__ import print_function
import os
import re
import random
import sys

parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
sys.path.append(parent_dir)
from grammar import Grammar

_N_MAIN_LINES = 1500
_N_EVENTHANDLER_LINES = 1


def generate_function_body(jsgrammar, num_lines):
    js = ''
    js += jsgrammar._generate_code(num_lines)
    return js


def GenerateNewSample(template, jsgrammar):
    result = template
    handlers = False
    while '<extfuzzer>' in result:
        numlines = _N_MAIN_LINES
        if handlers:
            numlines = _N_EVENTHANDLER_LINES
        else:
            handlers = True
        result = result.replace(
            '<extfuzzer>',
            generate_function_body(jsgrammar, numlines),
            1
        )
    return result


def load_grammar(grammar_dir, subsystem):
    """Build the Firefox grammar, optionally restricted to one subsystem.

    Without --subsystem the full grammar (all 23 api_firefox files, plus the
    shared ext_var / ext_callback / browser_extra rules) is loaded.
    With --subsystem <name> every rule stays defined, but only that
    subsystem's call candidates are emitted, so the generated code focuses on
    e.g. browser.tabs.* (helper variables like tab/window ids remain available).
    """
    jsgrammar = Grammar()
    jsgrammar._definitions_dir = grammar_dir
    main_path = os.path.join(grammar_dir, 'main_firefox.txt')
    if not subsystem:
        err = jsgrammar.parse_from_file(main_path)
        return err, jsgrammar

    text = open(main_path).read()

    # In subsystem mode the generic callback pool is filtered down to the
    # chosen namespace, otherwise callbacks keep pulling in every other
    # subsystem's API calls. Structural rules (no browser.* call) are kept.
    cb_path = os.path.join(grammar_dir, 'api_firefox', 'ext_callback.txt')
    cb_lines = []
    if os.path.exists(cb_path):
        ns_re = re.compile(r'browser\.([A-Za-z0-9_]+)\.')
        for cb in open(cb_path).read().split('\n'):
            cbs = cb.strip()
            if 'browser.' not in cbs:
                cb_lines.append(cb)
                continue
            if ('browser.' + subsystem + '.') not in cbs:
                continue
            # drop lines that also call another namespace (nested cross-calls)
            others = [m for m in ns_re.findall(cbs) if m != subsystem]
            if not others:
                cb_lines.append(cb)

    lines = []
    for line in text.split('\n'):
        ls = line.strip()
        # domato's <lines> rule is global (all !begin lines blocks merge), so
        # in subsystem mode we include ONLY the chosen subsystem's grammar file
        if ls.startswith('!include ./api_firefox/browser_'):
            fam = ls[len('!include ./api_firefox/browser_'):].replace('.txt', '')
            if fam != subsystem:
                continue
        if ls == '!include ./api_firefox/ext_callback.txt':
            lines.extend(cb_lines)
            continue
        if ls.startswith('<my_browser_'):
            name = ls[len('<my_browser_'):ls.find('>')]
            if name != subsystem:
                continue
        lines.append(line)
    err = jsgrammar.parse_from_string('\n'.join(lines))
    return err, jsgrammar


def generate_samples(grammar_dir, outfiles, subsystem):
    """Generates a set of samples and writes them to the output files."""

    f = open(os.path.join(grammar_dir, 'template_ext_firefox.html'))
    template = f.read()
    f.close()

    err, jsgrammar = load_grammar(grammar_dir, subsystem)
    if err > 0:
        print('There were errors parsing grammar')
        return

    for outfile in outfiles:
        result = GenerateNewSample(template, jsgrammar)
        if result is not None:
            print('Writing a sample to ' + outfile)
            try:
                f = open(outfile, 'w')
                f.write(result)
                f.close()
            except IOError:
                print('Error writing to output')


def get_option(option_name):
    for i in range(len(sys.argv)):
        if (sys.argv[i] == option_name) and ((i + 1) < len(sys.argv)):
            return sys.argv[i + 1]
        elif sys.argv[i].startswith(option_name + '='):
            return sys.argv[i][len(option_name) + 1:]
    return None


def main():
    fuzzer_dir = os.path.dirname(__file__)
    subsystem = get_option('--subsystem')

    multiple_samples = False
    for a in sys.argv:
        if a.startswith('--output_dir='):
            multiple_samples = True
    if '--output_dir' in sys.argv:
        multiple_samples = True

    if multiple_samples:
        print('Running on ClusterFuzz')
        out_dir = get_option('--output_dir')
        nsamples = int(get_option('--no_of_files'))
        print('Output directory: ' + out_dir)
        print('Number of samples: ' + str(nsamples))

        if not os.path.exists(out_dir):
            os.mkdir(out_dir)

        outfiles = []
        for i in range(nsamples):
            outfiles.append(os.path.join(out_dir, 'fuzz-' + str(i).zfill(5) + '.html'))

        generate_samples(fuzzer_dir, outfiles, subsystem)

    elif len(sys.argv) > 1:
        outfile = sys.argv[1]
        generate_samples(fuzzer_dir, [outfile], subsystem)

    else:
        print('Arguments missing')
        print("Usage:")
        print("\tpython generator_firefox.py <output file> [--subsystem <subsystem_name>]")
        print("\tpython generator_firefox.py --output_dir <output directory> --no_of_files <number of output files> [--subsystem <subsystem_name>]")

if __name__ == '__main__':
    main()