#!/usr/bin/python3 
# -*- coding: UTF-8 -*-

import sys,os,getopt
import subprocess,shutil,time,random
import profile
from subprocess import Popen, PIPE
import shlex
import threading
import argparse
from pathlib import Path
import json

def copy_js_folder(src_dir, dst_dir):
    src_js = src_dir / "js"
    dst_js = dst_dir / "js"
    if src_js.exists():
        shutil.copytree(src_js, dst_js, dirs_exist_ok=True)
        print(f"Copied js folder to {dst_js}")
    else:
        print(f"js folder not found in {src_js}")

def copy_manifest(src_dir, dst_dir):
    src_manifest = src_dir / "manifest.json"
    dst_manifest = dst_dir / "manifest.json"
    if src_manifest.exists():
        shutil.copy2(src_manifest, dst_manifest)
        print(f"Copied manifest.json to {dst_manifest}")
    else:
        print(f"manifest.json not found in {src_manifest}")

def copy_background(src_dir, dst_dir, as_main=False):
    src = src_dir / "background.js"
    dst = dst_dir / "background.js"
    if src.exists():
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dst)
        print(f"Copied {src} to {dst}")

def run_generator(script, output_file, extra_args):
    # print(script)
    # print(extra_args)
    try:
        result = subprocess.run(
            ["python2.7"] + script.split() + [str(output_file)] + extra_args.split(),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=True,
            timeout=120
        )
        if Path(output_file).exists():
            print(f"Generated {output_file}")
            return True
        else:
            print(f"Error: {output_file} was not created")
            print("STDOUT:", result.stdout.decode())
            print("STDERR:", result.stderr.decode())
            return False
    except subprocess.CalledProcessError as e:
        print(f"Error running generator: {e}")
        print("STDOUT:", e.stdout.decode() if e.stdout else "")
        print("STDERR:", e.stderr.decode() if e.stderr else "")
        return False
    except Exception as e:
        print(f"Error running generator: {e}")
        return False

def get_js_files_from_manifest(manifest_path):
    js_files = set()
    with open(manifest_path, "r", encoding="utf-8") as f:
        manifest = json.load(f)
    # background
    if "background" in manifest:
        js_files.add("js/main.js")
    # content_scripts
    if "content_scripts" in manifest:
        for cs in manifest["content_scripts"]:
            js_files.update(cs.get("js", []))
    # popup
    if "action" in manifest and "default_popup" in manifest["action"]:
        popup_html = manifest["action"]["default_popup"]
        #
        js_files.add("js/popup.js")
    if "browser_action" in manifest and "default_popup" in manifest["browser_action"]:
        popup_html = manifest["browser_action"]["default_popup"]
        js_files.add("js/popup.js")
    return js_files

def generate_sample(i, j, template_dir, out_dir, subsystem):
    target_dir = out_dir / str(i) / str(j)
    shutil.copytree(template_dir, target_dir)
    manifest_path = target_dir / "manifest.json"
    js_files = get_js_files_from_manifest(manifest_path)
    for js_file in js_files:
        js_path = target_dir / js_file
        js_path.parent.mkdir(parents=True, exist_ok=True)
        for _ in range(3):
            if run_generator("generator.py", js_path, f"--subsystem {subsystem}"):
                break



def main():
    parser = argparse.ArgumentParser(description="Generate Chrome extension samples.")
    parser.add_argument("-p", "--pattern", choices=["template"], required=True, help="Generation pattern")
    parser.add_argument("-n", "--number", type=int, required=True, help="Number of samples to generate")
    parser.add_argument("-t", "--templatefile", required=True, help="Template directory (required)")
    parser.add_argument("-o", "--outputdir", required=True, help="Output directory (required)")
    parser.add_argument("-s", "--subsystem", required=True, help="Subsystem (required)")
    args = parser.parse_args()

    if args.pattern == "template":
        out_dir = Path.cwd() / args.outputdir
        template_dir = Path(args.templatefile)
        for i in range(args.number):
            print(f"\n ## Generating extensions {i}")
            for j in range(random.randint(1, 5)):
                try:
                    generate_sample(i, j, template_dir, out_dir, args.subsystem)
                except Exception as e:
                    print(f"Generation failed: {e}")

if __name__ == "__main__":
    main()




