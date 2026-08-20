#!/usr/bin/python3
# -*- coding: UTF-8 -*-
"""TriChord - Firefox extension package generator.

Generates installable Firefox WebExtensions by copying the packaging
template (manifest.json, background.js, js/main.html), assigning each
extension a unique gecko.id, and filling js/main.js with a fuzz sample
from generator_firefox.py.

By default each group i contains 2-10 extensions (multi-extension
orchestration); use --ext-per-group to fix the count.
"""

import argparse
import json
import random
import shutil
import subprocess
import uuid
from pathlib import Path

MODULE_DIR = Path(__file__).resolve().parent
GENERATOR = MODULE_DIR / "generator_firefox.py"
DEFAULT_TEMPLATE = MODULE_DIR / "res" / "template_v2_01_firefox"


def run_generator(script, output_file, subsystem):
    cmd = ["python2.7", str(script), str(output_file)]
    if subsystem:
        cmd += ["--subsystem", subsystem]
    try:
        result = subprocess.run(cmd, stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE, check=True, timeout=300)
    except subprocess.CalledProcessError as e:
        print("Error running generator:")
        print(e.stdout.decode() if e.stdout else "")
        print(e.stderr.decode() if e.stderr else "")
        return False
    if Path(output_file).exists():
        print("Generated " + str(output_file))
        return True
    print("Error: " + str(output_file) + " was not created")
    return False


def get_js_files_from_manifest(manifest_path):
    js_files = set()
    with open(manifest_path, "r", encoding="utf-8") as f:
        manifest = json.load(f)
    if "background" in manifest:
        js_files.add("js/main.js")
    for key in ("action", "browser_action"):
        if key in manifest and "default_popup" in manifest[key]:
            js_files.add("js/popup.js")
    return js_files


def patch_manifest_id(manifest_path, ext_index):
    """Assign a unique gecko.id to each extension (required by Firefox)."""
    with open(manifest_path, "r", encoding="utf-8") as f:
        manifest = json.load(f)
    unique_id = "fuzz-ext-%d-%s@example.com" % (ext_index, uuid.uuid4().hex[:8])
    bss = manifest.setdefault("browser_specific_settings", {})
    bss.setdefault("gecko", {})["id"] = unique_id
    with open(manifest_path, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2)
    return unique_id


def generate_sample(i, j, template_dir, out_dir, subsystem):
    target_dir = out_dir / str(i) / str(j)
    shutil.copytree(str(template_dir), str(target_dir))
    manifest_path = target_dir / "manifest.json"
    addon_id = patch_manifest_id(manifest_path, j)
    print("  Extension %d: id=%s" % (j, addon_id))
    for js_file in get_js_files_from_manifest(manifest_path):
        js_path = target_dir / js_file
        js_path.parent.mkdir(parents=True, exist_ok=True)
        for _ in range(3):
            if run_generator(GENERATOR, js_path, subsystem):
                break


def main():
    parser = argparse.ArgumentParser(
        description="Generate Firefox extension samples with multi-extension groups.")
    parser.add_argument("-p", "--pattern", choices=["template"], required=True)
    parser.add_argument("-n", "--number", type=int, required=True,
                        help="Number of extension groups to generate")
    parser.add_argument("-t", "--templatefile", default=str(DEFAULT_TEMPLATE),
                        help="Template directory (default: res/template_v2_01_firefox)")
    parser.add_argument("-o", "--outputdir", required=True,
                        help="Output directory (relative to CWD)")
    parser.add_argument("-s", "--subsystem", default=None,
                        help="Subsystem to focus generation on (e.g. tabs)")
    parser.add_argument("--ext-per-group", type=int, default=None,
                        help="Fixed extensions per group (default: random 2-10)")
    args = parser.parse_args()

    if args.pattern == "template":
        out_dir = Path.cwd() / args.outputdir
        template_dir = Path(args.templatefile).resolve()
        if not template_dir.exists():
            print("Template not found: " + str(template_dir))
            return
        for i in range(args.number):
            ext_count = args.ext_per_group or random.randint(2, 10)
            print("\n ## Generating group %d with %d extensions (subsystem=%s)"
                  % (i, ext_count, args.subsystem))
            for j in range(ext_count):
                generate_sample(i, j, template_dir, out_dir, args.subsystem)


if __name__ == "__main__":
    main()