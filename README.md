# Image to WebP Converter 🚀

**Quickly convert your PNG, JPG, JPEG, TIFF, and BMP images to the modern WebP format. Optimize images for the web, reduce file sizes, and save disk space!**

This project offers a user-friendly Graphical User Interface (GUI) for easy, visual batch conversion of images. 

A command-line interface (CLI) is also offered to support automated workflows.

**Join our Discord community!** [https://discord.gg/HhBSvM9gBY](https://discord.gg/HhBSvM9gBY)

## Table of Contents

1.  [Features](#features)
2.  [Requirements](#requirements)
3.  [Getting Started: Installation](#getting-started-installation)
    *   [Prerequisites: Install Python](#prerequisites-install-python)
    *   [Setup Instructions](#setup-instructions)
4.  [How to Use the GUI](#how-to-use-the-gui)
5.  [Troubleshooting](#troubleshooting)
6.  [Contributing (Coming Soon)](#contributing-coming-soon)
7.  [License](#license)

## 1. Features

*   **Batch Image Conversion:** Convert entire folders of images to WebP.
*   **Single Image Conversion:** Select and convert individual image files.
*   **Recursive Folder Processing:** Option to process images within subfolders of your selected input folder.
*   **Flexible Output:**
    *   Save converted WebP images alongside the originals.
    *   Specify a separate output folder.
    *   Create new output subfolders directly from the GUI.
*   **WebP Quality Control:** Adjust the quality level (0-100) for lossy WebP compression.
*   **Lossless Compression:** Option for lossless WebP for maximum image fidelity.
*   **Overwrite Protection:** Choose whether to overwrite existing WebP files or skip them.
*   **Zip Output:** Automatically zip the contents of the output folder after conversion.
*   **Real-time Progress:** Visual progress bar and status log within the GUI.
*   **Theming:** Select from various light and dark themes for the GUI (requires `qt-material`).
*   **Adjustable Window Size:** Choose from predefined window sizes for comfortable viewing.

## 2. Requirements

To run the Image to WebP Converter GUI, you'll need the following Python libraries:

*   **`PyQt6`**: For the graphical user interface.
*   **`Pillow` (PIL Fork)**: For image processing and WebP conversion.
*   **`qt-material` (Optional but Recommended)**: For enhanced GUI themes and a modern look.

*The `tqdm` library is used by the `image_converter.py` backend for its standalone testing/CLI mode, but is not strictly required if you only use the GUI and the GUI's progress updates.*

## 3. Getting Started: Installation

Follow these steps to get the converter up and running on your system.

### Prerequisites: Install Python

If you don't have Python installed, you'll need to get it first. We recommend Python 3.8 or newer.

*   **Windows:**
    1.  Download the latest Python installer from [python.org/downloads/windows/](https://www.python.org/downloads/windows/).
    2.  Run the installer. **Important:** Check the box that says "Add Python to PATH" during installation.
*   **macOS:**
    *   Python often comes pre-installed. Open Terminal (Applications > Utilities > Terminal) and type `python3 --version`.
    *   If not installed or you need a newer version, you can download it from [python.org/downloads/mac-osx/](https://www.python.org/downloads/mac-osx/) or use a package manager like Homebrew (`brew install python3`).
*   **Linux:**
    *   Python is usually pre-installed. Open your terminal and type `python3 --version`.
    *   If not, use your distribution's package manager. For example, on Debian/Ubuntu:
        ```bash
        sudo apt update
        sudo apt install python3 python3-pip python3-venv
        ```

### Setup Instructions

1.  **Get the Code:**
    *   **Recommended (using Git):** If you have Git installed, clone the repository. This is the best way to get the code and easily update it later.
        ```bash
        git clone https://github.com/Ktiseos-Nyx/Webp_Gui_Converter WebPConverter 
        # Example: git clone https://github.com/Ktiseos-Nyx/Webp_Gui_Converter.git WebPConverter
        # This clones the repo into a folder named "WebPConverter"
        ```
        If you don't have Git, you can download it from [git-scm.com](https://git-scm.com/downloads).

    *   **Alternative (Download ZIP):**
        *   Go to the project's repository page (e.g., on GitHub).
        *   Click the "Code" button and select "Download ZIP".
        *   Extract the ZIP file to a folder on your computer (e.g., `C:\Users\YourName\Documents\WebPConverter` or `/home/yourname/WebPConverter`). Note that with this method, you'll need to re-download the ZIP to get updates.

2.  **Open a Terminal or Command Prompt:**
    *   **Windows:** Search for "Command Prompt" or "PowerShell".
    *   **macOS/Linux:** Open your Terminal application.
    *   Navigate to the folder where you cloned or extracted the project files:
        ```bash
        cd WebPConverter # Or the name you used
        ```

3.  **Create and Activate a Virtual Environment (Recommended):**
    This isolates the project's dependencies from your system's Python.
    ```bash
    python3 -m venv .venv  # Creates a virtual environment folder named .venv
    ```
    Activate it:
    *   **Windows (Command Prompt):**
        ```cmd
        .venv\Scripts\activate.bat
        ```
    *   **Windows (PowerShell):**
        ```powershell
        .venv\Scripts\Activate.ps1
        # If you get an error about execution policies, run:
        # Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process
        # Then try activating again.
        ```
    *   **macOS/Linux (bash/zsh):**
        ```bash
        source .venv/bin/activate
        ```
    Your terminal prompt should now show `(.venv)` at the beginning.

4.  **Install Dependencies:**
    With the virtual environment activated, you can install the required libraries.

    *   **Option A (Install key packages manually):** This installs the main libraries, and `pip` will automatically fetch their necessary sub-dependencies.
        ```bash
        pip install Pillow PyQt6
        ```
        For the enhanced themes (optional but highly recommended):
        ```bash
        pip install qt-material
        ```

    *   **Option B (Using `requirements.txt` for specific versions):** A `requirements.txt` file is provided in the project root. This file lists all necessary packages (including sub-dependencies) with specific versions known to work. Using this ensures a consistent environment.
        ```bash
        pip install -r requirements.txt
        ```

## 4. How to Use the GUI

Once the setup is complete:

1.  **Ensure your virtual environment is activated** (see step 3 in Setup).
2.  **Navigate to the project directory** in your terminal if you're not already there.
3.  **Run the GUI script:**
    ```bash
    python webp_gui.py  
    ```
    (The main GUI Python file is the one containing the `ImageConverterGUI` class).

**Using the Interface:**

*   **Input Folder/File:**
    *   Click "Browse..." next to "Input Folder/File".
    *   A dialog will ask if you want to "Select Folder" or "Select File".
    *   Choose accordingly to select either an entire folder of images or a single image file.
*   **Use Separate Output Folder (Checkbox):**
    *   **Unchecked (Default):** Converted WebP images will be saved in the same location as their original files (maintaining any subfolder structure if "Process Subfolders" is active).
    *   **Checked:** Allows you to specify a different folder for all converted WebP images.
        *   **Output Folder:** If the checkbox is checked, you can type a path or click "Browse..." to select an existing folder where all WebP files will be saved.
        *   **Create New Output Subfolder:** Click this to create a new subfolder within the currently selected Input or Output folder.
*   **WebP Quality (0-100):** Adjust the slider for lossy compression. Higher values mean better quality and larger files.
*   **Lossless Compression:** Check for perfect quality (larger files). Overrides the quality setting.
*   **Process Subfolders:** If your input is a folder, check this to also convert images in its subdirectories. The subfolder structure will be mirrored in the output location.
*   **Overwrite Existing WebP:**
    *   **Unchecked (Default):** If a WebP file with the same name already exists in the output location, it will be skipped.
    *   **Checked:** Existing WebP files will be overwritten.
*   **Zip Output After Conversion:** If "Use Separate Output Folder" is checked and an output folder is specified, this option will create a ZIP archive of the output folder's contents after conversion.
*   **Convert to WebP:** Click this button to start the conversion process.
*   **Progress Bar & Status Log:** Monitor the conversion progress and see detailed messages or any errors.
*   **Menu Bar (Top of Window):**
    *   **File > Exit:** Closes the application.
    *   **View > Set Window Size:** Choose from predefined window dimensions.
    *   **View > Theme:** (If `qt-material` is installed) Select a visual theme for the application.

## 5. Troubleshooting

*   **`DeprecationWarning: sipPyTypeDict() is deprecated...`:** This is a common warning with some PyQt6 versions. It's usually internal to the library and doesn't affect functionality. Try upgrading PyQt6: `pip install --upgrade PyQt6 PyQt6-sip`. If it persists and the app works, it can often be ignored.
*   **"ModuleNotFoundError: No module named 'X'"**: Make sure you have activated your virtual environment (`.venv`) before running `pip install` or `python your_gui_script_name.py`. Also, double-check that you've installed all required libraries listed in the "Requirements" section.
*   **GUI looks very basic/old:** You might not have `qt-material` installed, or it failed to apply a theme. Try installing it: `pip install qt-material`.
*   **Cannot select an input folder:** Ensure you are using the latest version of the GUI script. The "Browse..." button for input should now clearly ask if you want to select a folder or a file.

If you encounter other issues, please feel free to [open an issue on GitHub](link-to-your-github-issues-page) or ask in our Discord community.

## 6. Contributing (Coming Soon)

Information on how to contribute to the project will be added here. We welcome bug reports, feature suggestions, and code contributions!

## 7. License

This project is licensed under the [MIT License](LICENSE.txt).
