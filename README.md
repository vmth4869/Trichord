# Trichord

A grammar-based fuzzing tool for generating Chrome extension API test cases, based on [Domato](https://github.com/googleprojectzero/domato/commit/fadff396cc45d521cc594d3e2396e27e887b1963). This tool generates extension code that exercises various Chrome extension APIs for security testing and vulnerability discovery.

## Features

- **Grammar-based Generation**: Uses Domato context-free grammar rules to generate syntactically correct code
- **Multi-subsystem Support**: Supports fuzzing of multiple Chrome subsystems
- **Extension Package Generation**: Generates complete extension packages with manifest/js/html files
- **Automation Scripts**: Generates xdotool scripts for automated browser interaction
- **Template-based**: Supports multiple extension templates (Manifest V2 and V3)

## Requirements

- Python 2.7 (for `generator.py`)
- Python 3.x (for `genExtension.py`)

## Directory Structure

```
ChromeFuzzCode/
├── chrome_extension/          # Chrome extension fuzzing components
│   ├── api/                   # Grammar files for different Chrome APIs
│   │   ├── chrome_action.txt
│   │   ├── chrome_alarms.txt
│   │   ├── chrome_bookmarks.txt
│   │   ├── chrome_tabs.txt
│   │   └── ...                # More API grammar files
│   ├── res/                   # Extension templates
│   │   ├── template_v2_01/    # Manifest V2 template
│   │   ├── template_v3_01/    # Manifest V3 template
│   │   └── template_v3_02/    # Manifest V3 template
│   ├── generator.py           # JavaScript code generator
│   ├── genExtension.py        # Extension package generator
│   ├── template_ext.js        # JavaScript template
│   └── main.txt               # Main grammar rules
├── xdotool/            # xdotool automation scripts
│   ├── generator.py           # xdotool script generator
│   ├── template.sh            # xdotool template
│   └── xdotool.txt            # xdotool grammar rules
├── firefox/            # Firefox (WebExtensions) fuzzing components
│   ├── api_firefox/           # Firefox API grammar files (browser.* namespaces)
│   │   ├── browser_tabs.txt   # browser.tabs.* rules
│   │   ├── browser_runtime.txt# browser.runtime.* rules
│   │   ├── browser_alarms.txt
│   │   └── ...                # one file per subsystem
│   ├── res/                   # Packaging template
│   │   └── template_v2_01_firefox/  # MV2 template (manifest + gecko.id)
│   ├── generator_firefox.py   # Firefox JavaScript code generator
│   ├── genExtension_firefox.py# Firefox extension package generator
│   ├── template_ext_firefox.html # Firefox generator template (background page)
│   └── main_firefox.txt       # Main Firefox grammar rules
└── grammar.py                 # Core grammar from Domato
```

## Usage

### 1. Generate Single JavaScript Sample

Generate a single JavaScript file that exercises Chrome extension APIs:

```bash
cd chrome_extension
# Generate to a specific output file
python generator.py <output_file> --subsystem <subsystem_name>

# Generate multiple files to a directory
python generator.py --output_dir <output_directory> --no_of_files <number> --subsystem <subsystem_name>
```

**Example:**
```bash
python generator.py --output_dir out/ --no_of_files 10 --subsystem tabs
```

### 2. Generate Complete Extension Packages

Generate complete Chrome extension packages with manifest files and all necessary components:

```bash
python3 genExtension.py -p template -n <number> -t <template_dir> -o <output_dir> -s <subsystem>
```

**Arguments:**
- `-p, --pattern`: Generation pattern (currently supports `template`)
- `-n, --number`: Number of extension samples to generate
- `-t, --templatefile`: Template directory path (e.g., `res/template_v3_01`)
- `-o, --outputdir`: Output directory for generated extensions
- `-s, --subsystem`: Target Chrome API subsystem

**Example:**
```bash
cd chrome_extension
python3 genExtension.py -p template -n 10 -t res/template_v3_01 -o out/ -s tabs
```

### 3. Generate xdotool Automation Scripts

Generate shell scripts for automated browser interaction using xdotool:

```bash
# Generate a single script
cd xdotool
python generator.py <output_file>

# Generate multiple scripts
python generator.py --output_dir <output_directory> --no_of_files <number>
```

**Example:**
```bash
cd xdotool
python generator.py --output_dir out/ --no_of_files 10
```

### 4. Generate Firefox (WebExtensions) Test Cases

```bash
cd firefox
# Full grammar (all Firefox subsystems)
python generator_firefox.py <output_file>

# Focus on a single subsystem
python generator_firefox.py <output_file> --subsystem tabs

# Multiple files
python generator_firefox.py --output_dir <output_directory> --no_of_files <number> --subsystem <subsystem_name>
```

**Example:**
```bash
cd firefox
python generator_firefox.py out.html --subsystem bookmarks
```

### 5. Generate Complete Firefox Extension Packages

Generate installable Firefox extensions (multi-extension groups with unique
`gecko.id` per extension):

```bash
cd firefox
python3 genExtension_firefox.py -p template -n <groups> -o <output_dir> \
  -s <subsystem> [-t res/template_v2_01_firefox] [--ext-per-group <count>]
```

- `-n`: number of extension groups (each group contains 2-10 extensions by
  default, or `--ext-per-group` fixed count)
- `-t`: packaging template (default: `res/template_v2_01_firefox`)
- `-s`: focus the generated calls on a subsystem (e.g. `tabs`)

**Example:**
```bash
cd firefox
python3 genExtension_firefox.py -p template -n 5 -o out/ -s tabs
```
Each generated extension is an installable package (`manifest.json` with
`browser_specific_settings.gecko.id`, `background.js`, `js/main.html`) whose
`js/main.js` is a fuzz sample generated by `generator_firefox.py`.



## Bug Showcase

