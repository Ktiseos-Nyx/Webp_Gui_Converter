# Image to WebP Converter 🚀

**Quickly convert a folder of PNG and JPG images to WebP format to save space!**

This script provides both a command-line interface and a simple PyQt6 GUI for batch image conversion.

Our Discord:

https://discord.gg/HhBSvM9gBY


**Tools Used:**

*   **Python:** The scripting language.
*   **Pillow (PIL):** Image processing library.
*   **PyQt6 (Optional):** For the graphical user interface.
*   **uv:**  Fast package installer and resolver (like `pip`, but faster!).
*   **pyenv:** Python version management.

**Setup & Installation (using pyenv and uv):**

1.  **Install pyenv:** Follow the instructions for your operating system: [https://github.com/pyenv/pyenv#installation](https://github.com/pyenv/pyenv#installation)

2.  **Install your desired Python version:**
    ```bash
    pyenv install 3.11  # Or your preferred Python version
    pyenv local 3.11    # Set this project to use Python 3.11
    ```

3.  **Install uv (and create a virtual environment):**
    ```bash
    python -m venv .venv  # Create a virtual environment named '.venv'
    source .venv/bin/activate  # Activate the virtual environment (Linux/macOS)
    .venv\Scripts\activate  # Activate the virtual environment (Windows)
    python -m pip install uv # Install uv inside the virtual environment
    ```

4.  **Install project dependencies using uv:**
    ```bash
    uv pip install -r requirements.txt  # If you have a requirements.txt
    # OR (if you don't have requirements.txt, install Pillow and PyQt6 directly if needed)
    uv pip install pillow  # For core functionality
    uv pip install pyqt6   # For the GUI (optional)
    ```
    **(Make sure to create a `requirements.txt` file with `pillow` and optionally `pyqt6` if you plan to distribute this!)**

**Usage:**

**1. Command-Line Interface (CLI):**

   ```bash
   python webp_converter.py  # Run the command-line script

   # Follow the prompts to enter:
   # - Input folder path
   # - Output folder path (optional, leave blank for input folder)
   # - WebP quality (default 80)
   # - Lossless compression (yes/no, default no)
   ```

**2. Graphical User Interface (GUI):**
   ```bash
python webp_converter_gui.py  # Run the GUI script
   ```

- Use the GUI to browse and select input/output folders, set quality, and choose lossless compression.

- Click "Convert Images" to start the process. Status messages will be displayed in the output area.


