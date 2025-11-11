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


## Bug Showcase

