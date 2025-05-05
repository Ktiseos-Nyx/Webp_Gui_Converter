# Image to WebP Converter 🚀

**Quickly convert folders or individual PNG and JPG images to WebP format, optimizing images for the web and saving disk space.**

This project provides two interfaces for batch image conversion: a command-line interface (CLI) for automated conversions and a PyQt6-based graphical user interface (GUI) for ease of use.

**Join our Discord community!** [https://discord.gg/HhBSvM9gBY](https://discord.gg/HhBSvM9gBY)

## Table of Contents

1.  [Features](#features)
2.  [Dependencies and Tools](#dependencies-and-tools)
    *   [Core Dependencies](#core-dependencies)
    *   [Optional Enhancements](#optional-enhancements)
3.  [Getting Started: Setup and Installation](#getting-started-setup-and-installation)
    *   [Prerequisites](#prerequisites)
    *   [Option 1: Recommended Setup (pyenv and uv)](#option-1-recommended-setup-pyenv-and-uv)
    *   [Option 2: Standard Setup (venv and pip)](#option-2-standard-setup-venv-and-pip)
    *   [Creating a `requirements.txt` File](#creating-a-requirementstxt-file)
4.  [Usage](#usage)
    *   [Command-Line Interface (CLI)](#command-line-interface-cli)
    *   [Graphical User Interface (GUI)](#graphical-user-interface-gui)

## 1. Features

*   **Batch Image Conversion:** Convert entire folders of images to WebP format.
*   **Single Image Conversion:** Convert individual images to WebP format.
*   **Recursive Folder Processing:** Process images in subfolders (CLI and GUI).
*   **Output Folder Selection:** Specify a separate output folder or save WebP images in the input folder.
*   **Create New Output Folder:** Create new output folders directly from the GUI.
*   **WebP Quality Control:** Adjust the quality level for lossy WebP compression (0-100).
*   **Lossless Compression:** Choose lossless WebP compression for maximum quality.
*   **File Overwrite Control:** Prevent overwriting existing files during conversion.
*   **Zip Output Folder:** Automatically zip the output folder after conversion (GUI only).
*   **Progress Reporting:** Display progress bars in both the CLI and GUI.
*   **Command-Line Interface (CLI):** For automated conversions and scripting.
*   **Graphical User Interface (GUI):** For ease of use and visual feedback.

## 2. Dependencies and Tools

This project utilizes several tools and libraries, categorized for clarity:

### ⚙️ Core Dependencies

*   **Python:** The scripting language used for the project. Its cross-platform nature ensures wide compatibility.
*   **Pillow (PIL):** The image processing library that handles the core conversion to WebP, offering fine-grained control over quality and compression.
*   **tqdm:** A library for displaying progress bars in the CLI.

### ✨ Optional Enhancements

*   **PyQt6:** (For GUI) A robust framework for creating the graphical user interface, providing a visual alternative to the CLI.
*   **uv (Recommended):** A significantly faster alternative to `pip` and `venv` for package management and virtual environment creation.
*   **pyenv (Recommended):** Allows for easy management of multiple Python versions, preventing conflicts between projects.
*   **pip:** The standard Python package installer (if not using `uv`).
*   **venv:** Python's built-in module for creating virtual environments (if not using `uv`).

## 3. Getting Started: Setup and Installation

Choose **one** of the setup options below. `pyenv` and `uv` are recommended for speed and best practices, but standard Python tools (`pip` and `venv`) are fully supported.

### Prerequisites

Before installation, make sure Python is installed. Open a terminal and run:

```bash
python --version  # or python3 --version
```
If Python is not found, install it:

*   Windows: Download from https://www.python.org/downloads/windows/ (remember to check "Add Python to PATH").

*   macOS: Install via Homebrew:

```bash
brew install python3
```

*   Linux: Use your distribution's package manager (e.g., sudo apt update && sudo apt install python3 python3-pip on Debian/Ubuntu).

#### Option 1: Recommended Setup (pyenv and uv)

Install pyenv: Follow instructions for your OS: https://github.com/pyenv/pyenv#installation.

For Windows, use pyenv-win: https://github.com/pyenv-win/pyenv-win.

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

#### Option 2: Standard Setup (venv and pip)

Ensure Python is Installed (See Prerequisites).

##### Create Virtual Environment:

```bash
python -m venv .venv
.venv\Scripts\Activate.ps1  # Windows (PowerShell)
```

OR

```bash
source .venv/bin/activate # Linux/macOS
```


##### Install Dependencies with pip:

```bash
python -m pip install pillow tqdm
python -m pip install pyqt6   # If using the GUI
```

#### Creating a requirements.txt File

You can create a requirements.txt file to easily install all dependencies:

```bash
python -m pip freeze > requirements.txt
```

##### Install the dependencies using:

```bash
python -m pip install -r requirements.txt
```

## 4. Usage

### Command-Line Interface (CLI)

The CLI (cli_script.py) provides a text-based interface for converting images.

**Run the Script:**

```bash
python cli_script.py <input_path> [options]
```
Arguments:

```bash
<input_path>: The path to the input folder or a single image file.
```
**Options:**
*   -o, --output_dir: The path to the output directory (optional). If not specified, the output will be saved in the input folder.
*   -q, --quality: The WebP quality (0-100, default 80).
*   -l, --lossless: Use lossless compression.
*   -r, --recursive: Process subfolders recursively.
*   -n, --no_overwrite: Prevent overwriting existing files.

**Example:**

```bash
python cli_script.py /path/to/images -o /path/to/output -q 90 -l -r -n
```
### Graphical User Interface (GUI)

The GUI (gui_script.py) offers a visual interface for converting images.

Run the Script:

```bash
python webp_gui.py
```
#### :**Use the GUI::**

*   Select Input Folder: Use the "Browse Input..." button to select the folder containing the images you want to convert.

*   Select Output Folder (Optional):

*   Check the "Use Separate Output Folder" checkbox.

*   Use the "Browse Output..." button to select an existing output folder.

*   Alternatively, click the "Create New Output Folder..." button to create a new folder.

*   Adjust Quality (Optional): Use the spinbox to set the desired WebP quality (0-100).

*   Choose Compression and Processing Options (Optional): Check the "Lossless Compression", "Process Subfolders Recursively", and "Overwrite Existing Files" checkboxes as needed.

*   Zip Output Folder (Optional): Check the "Zip Output Folder After Conversion" checkbox to automatically zip the output folder after the conversion is complete.

*   Click "Convert Images": Start the conversion process.

*   Monitor Status: View the progress and any error messages in the status output area.

Note: On macOS, the "Create New Output Folder..." button will open a Finder window, where you need to manually create a new folder and then select it.




