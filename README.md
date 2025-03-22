# Image to WebP Converter 🚀

**Quickly convert folders of PNG and JPG images to WebP format, optimizing images for the web and saving disk space.**

This project provides two interfaces for batch image conversion: a command-line interface (CLI) for automated conversions and a PyQt6-based graphical user interface (GUI) for ease of use.

**Join our Discord community!** [https://discord.gg/HhBSvM9gBY](https://discord.gg/HhBSvM9gBY)

## Table of Contents

1.  [Dependencies and Tools](#dependencies-and-tools)
    *   [Core Dependencies](#core-dependencies)
    *   [Optional Enhancements](#optional-enhancements)
2.  [Getting Started: Setup and Installation](#getting-started-setup-and-installation)
    *   [Prerequisites](#prerequisites)
    *   [Option 1: Recommended Setup (pyenv and uv)](#option-1-recommended-setup-pyenv-and-uv)
    *   [Option 2: Standard Setup (venv and pip)](#option-2-standard-setup-venv-and-pip)
    *   [Creating a `requirements.txt` File](#creating-a-requirementstxt-file)
3.  [Usage](#usage)
    *   [Command-Line Interface (CLI)](#command-line-interface-cli)
    *   [Graphical User Interface (GUI)](#graphical-user-interface-gui)

## 1. Dependencies and Tools

This project utilizes several tools and libraries, categorized for clarity:

### ⚙️ Core Dependencies

*   **Python:**  The scripting language used for the project.  Its cross-platform nature ensures wide compatibility.
*   **Pillow (PIL):**  The image processing library that handles the core conversion to WebP, offering fine-grained control over quality and compression.

### ✨ Optional Enhancements

*   **PyQt6:** (For GUI)  A robust framework for creating the graphical user interface, providing a visual alternative to the CLI.
*   **uv (Recommended):** A significantly faster alternative to `pip` and `venv` for package management and virtual environment creation.
*   **pyenv (Recommended):**  Allows for easy management of multiple Python versions, preventing conflicts between projects.
*   **pip:**  The standard Python package installer (if not using `uv`).
*   **venv:**  Python's built-in module for creating virtual environments (if not using `uv`).

## 2. Getting Started: Setup and Installation

Choose **one** of the setup options below.  `pyenv` and `uv` are recommended for speed and best practices, but standard Python tools (`pip` and `venv`) are fully supported.

### Prerequisites

Before installation, make sure Python is installed. Open a terminal and run:

```bash
python --version  # or python3 --version
Use code with caution.
If Python is not found, install it:
```
> Windows: Download from 

https://www.python.org/downloads/windows/ 

(remember to check "Add Python to PATH").

> macOS:
Install via Homebrew: 
``` bash 
brew install python3
```
(https://brew.sh/)

> Linux: Use your distribution's package manager (e.g., sudo apt update && sudo apt install python3 python3-pip on Debian/Ubuntu).

#### Option 1: Recommended Setup (pyenv and uv)

Install pyenv: Follow instructions for your OS: 
https://github.com/pyenv/pyenv#installation. 

> For Windows, use pyenv-win: https://github.com/pyenv-win/pyenv-win.

Install Python Version (e.g., 3.11):

```bash
pyenv install 3.11
pyenv local 3.11  # Set this project to use 3.11
```

Install uv and Create Virtual Environment:
```bash
python -m venv .venv  # Create virtual environment
.venv\Scripts\Activate.ps1  # Windows (PowerShell)
```
OR
```bash
source .venv/bin/activate # Linux/macOS
python -m pip install uv  # Install uv *inside* the venv
```
Install Dependencies with uv:
```bash
uv pip install pillow  # For core functionality
uv pip install pyqt6   # If using the GUI
``` 

#### Option 2: Standard Setup (venv and pip)
Ensure Python is Installed (See Prerequisites).

Create Virtual Environment:
```bash
python -m venv .venv
.venv\Scripts\Activate.ps1  # Windows (PowerShell)
``` 
 OR
```bash
source .venv/bin/activate # Linux/macOS
``` 
Install Dependencies with pip:
```bash
python -m pip install -r requirements.txt  # If you have a requirements.txt
``` 
OR
```bash
python -m pip install pillow
python -m pip install pyqt6   # If using the GUI
```

Run the Script:
``` bash
python webp_cli_converter.py
```
# Command Line Interface CLI

Follow the Prompts:

Input Folder: Provide the full path to the folder with your images.

Output Folder: Enter the path for the WebP files. Leave blank to save in the input folder (replacing originals!).

Quality: Enter a value (0-100, default 80). Press Enter for the default.

Lossless: Type yes for lossless compression (larger files, perfect quality), or no (default, lossy compression). Press enter for the default.

The script will print progress and error messages.

# Graphical User Interface (GUI)
The GUI (webp_converter_gui.py) offers a visual interface.

Run the Script:
``` bash
python webp_converter_gui.py
Use code with caution.
``` 
Use the GUI:

Select Input/Output Folders: Use the browse buttons.

Adjust Quality (Optional): Use the slider/input field.

Lossless/Recursive (Optional): Check the boxes as needed.

Click "Convert Images": Start the conversion.

Monitor Status: View progress in the output area.
