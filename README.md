# Image to WebP Converter 🚀

**Quickly convert folders of PNG and JPG images to WebP format, reclaiming precious disk space and optimizing your web assets!**

This script offers both a user-friendly command-line interface (CLI) for streamlined, scriptable conversions and a straightforward PyQt6 Graphical User Interface (GUI) for those who prefer a visual, point-and-click experience. Whether you're a command-line ninja or a GUI enthusiast, this tool has you covered for efficient batch image conversion to the modern WebP format.

Our vibrant community awaits you on Discord! Join us to share your experiences, ask questions, contribute ideas, and connect with fellow users:

[https://discord.gg/HhBSvM9gBY](https://discord.gg/HhBSvM9gBY)

## 🛠️ Dependencies and Tools: A Deep Dive

To ensure a smooth and successful experience with the Image to WebP Converter, it's crucial to understand the tools and libraries that power it. This section provides a detailed breakdown of each component, categorized by its role in the project.

### ⚙️ Core Dependencies: The Engine Room

These are the fundamental building blocks, the essential libraries without which the Image to WebP Converter simply cannot function. They form the bedrock of the script's core functionality.

*   **Python:** The Versatile Scripting Maestro

    *   **Role:** Python is the beating heart of this project, the high-level, interpreted programming language in which the entire script is written. Its readability, extensive standard library, and vast ecosystem of third-party packages make it an ideal choice for tasks ranging from simple scripting to complex application development. Python's cross-platform nature ensures that the converter can run seamlessly on Windows, macOS, and Linux environments, providing broad accessibility to users across different operating systems.
    *   **Why Python?** Python's strengths lie in its ease of use, rapid development capabilities, and a rich set of libraries for diverse tasks. For image processing and GUI development, Python's ecosystem is particularly robust, making it a perfect fit for this project. Its clear syntax reduces development time and enhances maintainability, crucial for a project designed for user-friendliness and long-term utility.

*   **Pillow (PIL):** The Image Processing Powerhouse

    *   **Role:** Pillow, derived from the Python Imaging Library (PIL), is the workhorse for image manipulation within the converter. It's a comprehensive image processing library that provides extensive capabilities for opening, manipulating, and saving a wide array of image file formats, including PNG, JPG, and, most importantly, WebP. Pillow is the engine that performs the actual image conversion, resizing, and quality adjustments, making it the core image processing component.
    *   **Why Pillow?** Pillow is chosen for its robust feature set, performance, and excellent WebP support. It offers fine-grained control over WebP encoding parameters, such as quality, lossless compression, and metadata handling, allowing for optimized WebP conversion tailored to different needs. Pillow's widespread adoption and active development ensure reliability and continuous improvement, making it a dependable choice for image processing tasks. Its ability to handle various image formats and perform complex manipulations makes it indispensable for this converter.

### ✨ Optional Enhancements: Elevating the Experience

These tools are not strictly required for the basic functionality of the Image to WebP Converter, but they significantly enhance the user experience, improve performance, or provide alternative setup methods. They offer flexibility and cater to different user preferences and technical environments.

*   **PyQt6:** The Cross-Platform GUI Framework

    *   **Role:** PyQt6 is a powerful Python binding for the Qt 6 application development framework. It enables the creation of visually appealing and highly functional Graphical User Interfaces (GUIs). In this project, PyQt6 is used to build the optional GUI application, providing a user-friendly alternative to the command-line interface. The GUI simplifies the conversion process for users who prefer visual interaction, allowing them to select folders, adjust settings, and initiate conversions with point-and-click ease.
    *   **Why PyQt6?** PyQt6 stands out for its cross-platform compatibility, rich set of widgets, and excellent performance in creating desktop applications. It allows for the development of native-looking GUIs that seamlessly integrate with the user's operating system, whether it's Windows, macOS, or Linux. PyQt6's extensive documentation and large community support make it a reliable choice for GUI development in Python, ensuring a robust and maintainable graphical interface for the Image to WebP Converter. Its advanced features allow for customization and creation of sophisticated user interfaces, enhancing the overall usability of the tool.

*   **uv (Optional, Recommended):** The Blazing-Fast Package Manager and Resolver

    *   **Role:** `uv` is a modern, extremely fast Python package installer and resolver, designed as a drop-in replacement for `pip` and `virtualenv`. It significantly accelerates the process of creating virtual environments and installing Python packages. While `pip` and `venv` are the standard tools, `uv` offers a substantial performance boost, especially for projects with many dependencies. It streamlines the setup process, reducing wait times and making the initial project setup much quicker and more efficient.
    *   **Why uv?** `uv` is recommended for its unparalleled speed and efficiency in package management. In development workflows, time is of the essence, and `uv` drastically reduces the time spent on environment setup and dependency installation. Its speed advantage is particularly noticeable in larger projects or when setting up environments frequently. By using `uv`, users can experience a significantly faster and smoother setup process, enhancing productivity and reducing frustration associated with dependency management. While `pip` and `venv` are perfectly functional, `uv` represents a leap forward in performance and developer experience.

*   **pyenv (Optional):** The Python Version Virtuoso

    *   **Role:** `pyenv` is a powerful Python version management tool. It allows you to effortlessly switch between multiple Python versions on the same system. This is particularly useful for developers who work on projects requiring different Python versions or who want to test their code against various Python interpreters. `pyenv` isolates Python versions, preventing conflicts and ensuring that each project can use its specified Python version without interference from others. It provides a clean and organized way to manage Python environments on your development machine.
    *   **Why pyenv?** `pyenv` is invaluable for maintaining isolated and consistent Python environments. It addresses the common issue of Python version conflicts, allowing you to easily manage and switch between different Python interpreters. This is crucial for ensuring project reproducibility and compatibility, especially when collaborating with others or deploying projects to different environments. `pyenv` promotes best practices in Python development by encouraging the use of specific Python versions for each project, leading to more stable and predictable development workflows. While not strictly necessary for running the converter, `pyenv` significantly enhances development environment management.

*   **pip:** The Standard Python Package Installer (Fallback)

    *   **Role:** `pip` is the default package installer for Python. It's used to install and manage packages from the Python Package Index (PyPI) and other indexes. While `uv` is recommended for its speed, `pip` remains a fully functional and widely used tool for package installation. In this project, `pip` serves as the standard, reliable option for users who may not be ready to adopt `uv` or prefer the traditional package management approach. It ensures that the project can be set up using widely available and well-documented tools.
    *   **Why pip?** `pip` is included as the standard and universally available package installer. It's pre-installed with most Python distributions and is extensively documented and supported. For users who are familiar with `pip` or prefer to use standard tools, it provides a straightforward way to install project dependencies. While it may not be as fast as `uv`, `pip` is a robust and dependable package manager that has been the mainstay of the Python ecosystem for years. Its inclusion ensures broad compatibility and ease of use for users who prefer the traditional Python tooling.

*   **venv:** The Standard Virtual Environment Module (Fallback)

    *   **Role:** `venv` is Python's built-in module for creating virtual environments. Virtual environments are isolated Python environments that allow you to install packages specific to a project without affecting the system-wide Python installation or other projects. `venv` is crucial for maintaining project dependencies in isolation, preventing conflicts between different project requirements. It's a standard practice in Python development to use virtual environments, and `venv` provides a readily available and reliable way to create them.
    *   **Why venv?** `venv` is included as the standard and built-in virtual environment tool. It's part of the Python standard library, ensuring its availability in any Python installation. For users who prefer to use standard Python tools or are not yet familiar with `uv`, `venv` provides a simple and effective way to create virtual environments. While `uv` offers faster environment creation, `venv` is a well-established and widely understood tool that serves the purpose of dependency isolation effectively. Its inclusion ensures that the project setup can be achieved using only core Python tools, without relying on external, potentially less familiar utilities.

## 🚀 Getting Started: Setup and Installation

Choose **one** of the following setup methods based on your technical preference and desired workflow. We highly recommend using `pyenv` and `uv` for a significantly faster and cleaner experience, especially if you are a frequent Python user or value development efficiency. However, standard Python tools (`venv` and `pip`) are also fully supported and provide a reliable alternative.

### Prerequisites: Ensuring Python is Ready

Before proceeding with either setup option, ensure that you have Python installed on your system.

*   **Checking for Python:** Open your terminal or command prompt and type:

    ```bash
    python --version
    ```

    or

    ```bash
    python3 --version
    ```

    If Python is installed, this command will display the Python version. If you encounter an error or Python is not recognized, you need to install Python.

*   **Installing Python:**

    *   **Windows:** Download the latest Python installer from the official Python website: [https://www.python.org/downloads/windows/](https://www.python.org/downloads/windows/). Run the installer and **make sure to check the box "Add Python to PATH"** during installation. This is crucial for being able to run Python commands from your terminal.

    *   **macOS:** macOS usually comes with Python pre-installed, but it's often an older version. It's highly recommended to install a more recent version using a package manager like Homebrew:

        ```bash
        brew install python3
        ```

        If you don't have Homebrew installed, you can install it from: [https://brew.sh/](https://brew.sh/)

    *   **Linux:** The installation process varies depending on your distribution. Use your distribution's package manager:

        *   **Debian/Ubuntu:**

            ```bash
            sudo apt update
            sudo apt install python3 python3-pip
            ```

        *   **Fedora/CentOS/RHEL:**

            ```bash
            sudo dnf install python3 python3-pip
            ```

        *   **Arch Linux:**

            ```bash
            sudo pacman -S python python-pip
            ```

    After installing Python, re-run the version check command (`python --version` or `python3 --version`) to confirm that Python is correctly installed and accessible.

### Option 1: Recommended Setup - Unleashing Speed with pyenv and uv (Fast & Isolated)

This setup leverages `pyenv` for isolated Python version management and `uv` for lightning-fast package installation and virtual environment creation. It's the preferred method for a streamlined and efficient development experience.

1.  **Install pyenv: The Python Version Manager**

    *   Follow the installation instructions specific to your operating system from the official pyenv repository: [https://github.com/pyenv/pyenv#installation](https://github.com/pyenv/pyenv#installation). The installation process typically involves cloning the pyenv repository and setting up environment variables in your shell configuration file (e.g., `.bashrc`, `.zshrc`, `.bash_profile`).

    *   **Example for Linux/macOS (using bash):**

        ```bash
        curl https://pyenv.run | bash
        echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.bashrc
        echo 'export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.bashrc
        echo 'eval "$(pyenv init -)"' >> ~/.bashrc
        source ~/.bashrc # Reload your shell configuration
        ```

        **For Windows users**, the recommended way to install `pyenv` is using `pyenv-win`: [https://github.com/pyenv-win/pyenv-win](https://github.com/pyenv-win/pyenv-win). Follow the installation instructions provided in the `pyenv-win` repository.

2.  **Install Your Desired Python Version using pyenv**

    *   List available Python versions that `pyenv` can install:

        ```bash
        pyenv install --list
        ```

    *   Install your preferred Python version. For example, to install Python 3.11:

        ```bash
        pyenv install 3.11
        ```

        Replace `3.11` with your desired Python version. `pyenv` will download and install the specified Python version in its isolated environment.

    *   Set the local Python version for your project directory. Navigate to the root directory of your `Image to WebP Converter` project in your terminal and run:

        ```bash
        pyenv local 3.11
        ```

        This command creates a `.python-version` file in your project directory, specifying that this directory and its subdirectories should use Python 3.11 (or the version you installed). When you are in this directory, `pyenv` will automatically switch to the specified Python version.

3.  **Install uv: The Ultrafast Package Manager (and Create a Virtual Environment)**

    *   `uv` excels at both package installation and virtual environment creation. While `uv` can manage virtual environments implicitly, it's still good practice to create an explicit virtual environment for project isolation.

    *   Create a virtual environment named `.venv` in your project directory using Python (even though we'll use `uv` later, we use standard Python to initially install `uv` within the virtual environment):

        ```bash
        python -m venv .venv
        ```

    *   Activate the virtual environment:

        *   **Windows (PowerShell):**

            ```powershell
            .venv\Scripts\Activate.ps1
            ```

        *   **Linux/macOS (bash/zsh):**

            ```bash
            source .venv/bin/activate
            ```

            Your terminal prompt should now be prefixed with `(.venv)`, indicating that the virtual environment is active.

    *   Install `uv` within the activated virtual environment using `pip` (since `uv` itself is a package installed via `pip` initially):

        ```bash
        python -m pip install uv
        ```

        **Important Note:** We are installing `uv` *inside* the virtual environment we just created. This ensures that `uv` is available within this isolated project environment.

4.  **Install Project Dependencies using uv: Experience the Speed!**

    *   Navigate to your project directory in the terminal (if you are not already there) and ensure your virtual environment is activated (`(.venv)` in your prompt).

    *   If you have a `requirements.txt` file (which is highly recommended for specifying project dependencies), install all dependencies listed in it using `uv`:

        ```bash
        uv pip install -r requirements.txt
        ```

        **What is `requirements.txt`?**  A `requirements.txt` file is a text file that lists all the Python packages your project depends on, along with their versions (optionally). It's a standard way to specify project dependencies, making it easy to reproduce the same environment on different machines or at different times. You should create a `requirements.txt` file and include `pillow` and `pyqt6` (if you want GUI support) in it.

        **Example `requirements.txt` content:**

        ```
        pillow
        pyqt6  # Optional for GUI support
        ```

    *   **Alternatively**, if you don't have a `requirements.txt` file yet, you can install `pillow` (for core functionality) and `pyqt6` (for the GUI, if desired) directly using `uv`:

        ```bash
        uv pip install pillow  # Install Pillow for core image conversion
        uv pip install pyqt6   # Install PyQt6 for the GUI (optional)
        ```

        `uv` will download and install the specified packages and their dependencies with remarkable speed.

### Option 2: Standard Setup - Utilizing venv and pip (Reliable & Familiar)

This setup uses Python's built-in `venv` module for virtual environment creation and the standard `pip` package installer. It's a more traditional approach, widely understood and readily available in all Python installations.

1.  **Ensure Python is Installed (Refer to Prerequisites Section)**

    *   If you haven't already, follow the instructions in the "Prerequisites: Ensuring Python is Ready" section to install Python on your system.

2.  **Create a Virtual Environment using venv**

    *   Navigate to your project directory in your terminal or command prompt.

    *   Create a virtual environment named `.venv`:

        ```bash
        python -m venv .venv
        ```

    *   Activate the virtual environment:

        *   **Windows (PowerShell):**

            ```powershell
            .venv\Scripts\Activate.ps1
            ```

        *   **Linux/macOS (bash/zsh):**

            ```bash
            source .venv/bin/activate
            ```

            Again, your terminal prompt will change to indicate the active virtual environment `(.venv)`.

3.  **Install Project Dependencies using pip**

    *   Ensure your virtual environment is activated (`(.venv)` in your prompt).

    *   If you have a `requirements.txt` file, install dependencies from it using `pip`:

        ```bash
        python -m pip install -r requirements.txt
        ```

    *   Alternatively, if you don't have a `requirements.txt` file, install `pillow` and `pyqt6` (if needed) directly using `pip`:

        ```bash
        python -m pip install pillow  # Install Pillow for core image conversion
        python -m pip install pyqt6   # Install PyQt6 for GUI (optional)
        ```

        `pip` will download and install the packages and their dependencies from PyPI.

**Creating a `requirements.txt` file (Recommended for both options):**

It's highly recommended to create a `requirements.txt` file to manage your project dependencies. This file makes it easy to share your project and ensure consistent environments.

1.  **After installing your dependencies (using either `uv pip install` or `python -m pip install`), you can generate a `requirements.txt` file by running:**

    ```bash
    python -m pip freeze > requirements.txt
    ```

    or

    ```bash
    uv pip freeze > requirements.txt # If you used uv to install
    ```

    This command will list all installed packages in your virtual environment and their versions, and save them to the `requirements.txt` file.

2.  **Place the `requirements.txt` file in the root directory of your project.**

Now, when you or someone else sets up the project, they can simply run `uv pip install -r requirements.txt` or `python -m pip install -r requirements.txt` to install all the necessary dependencies, ensuring a consistent environment.

## ⚙️ Usage: Converting Images to WebP

Once you have completed the setup and installation process, you are ready to use the Image to WebP Converter! You can choose between the Command-Line Interface (CLI) for scriptable, automated conversions or the Graphical User Interface (GUI) for a more interactive, visual experience.

### 1. Command-Line Interface (CLI): Interactive Conversion via Prompts

The Command-Line Interface (CLI) for the Image to WebP Converter, `webp_cli_converter.py`, is designed for **interactive use**.  Instead of providing command-line arguments directly when you run the script, it will **prompt you step-by-step** for the information it needs to perform the image conversion. This makes it incredibly easy to use, even if you're not a command-line expert!

*   **Running the CLI Script:** Open your terminal or command prompt, navigate to the directory where you have saved `webp_cli_converter.py`, ensure your virtual environment is activated (if you set one up), and then execute the script using Python:

    ```bash
    python webp_cli_converter.py
    ```

    Simply type this command and press Enter. The script will then start guiding you through the conversion process with a series of prompts.

*   **Interactive Prompts and Options:**  Once you run the script, it will engage you with the following prompts, one after another. You'll need to provide input for each prompt to configure your image conversion:

    1.  **"Enter the path to the input folder containing images:"**

        *   **Action:**  Carefully type or paste the **full path** to the folder that holds the PNG and JPG images you want to convert to WebP.
        *   **Example:**  If your images are in a folder named `my_images` located in your `Documents` directory on Windows, you might enter something like: `C:\Users\YourUsername\Documents\my_images`  (Windows example). On macOS or Linux, it might look like: `/Users/yourusername/Documents/my_images`.
        *   **Press Enter** after typing the input folder path.

    2.  **"Enter the path to the output folder (leave blank to save in input folder):"**

        *   **Action:**  This prompt lets you decide where the converted WebP images should be saved. You have two choices:
            *   **Save in the Input Folder:** If you want the WebP images to be saved in the *same folder* as your original PNG and JPG images (effectively replacing them with WebP versions, so be cautious!), simply **press Enter without typing anything**. The script will default to saving the WebP files in the input folder you specified in the previous step.
            *   **Save in a Different Output Folder:** If you want to keep your original images untouched and save the WebP versions in a *separate folder*, type or paste the **full path** to the desired output folder here.  If the output folder you specify doesn't exist yet, the script will automatically create it for you.
        *   **Example (Saving in a separate folder):**  `C:\Users\YourUsername\Documents\webp_output` (Windows) or `/Users/yourusername/Documents/webp_output` (macOS/Linux).
        *   **Press Enter** after typing the output folder path (or just press Enter to save in the input folder).

    3.  **"Enter WebP quality (0-100, default 80):"**

        *   **Action:** This prompt controls the quality of the converted WebP images.  WebP uses lossy compression by default (unless you choose lossless). The quality value ranges from 0 to 100, where:
            *   **100:**  Best possible quality (largest file size).
            *   **0:**   Lowest quality (smallest file size, potentially significant quality loss).
            *   **80 (Default):** A good balance between quality and file size, suitable for most web use cases.
        *   **To use the default quality of 80, simply press Enter without typing anything.**
        *   **To specify a different quality level**, type a number between 0 and 100 (inclusive).  For example, `90` for slightly higher quality than the default, or `70` for smaller file sizes if you're optimizing aggressively for web performance and can tolerate a slight quality reduction.
        *   **Press Enter** after typing the quality value (or just press Enter to use the default quality of 80).

    4.  **"Use lossless WebP compression? (yes/no, default no):"**

        *   **Action:** This prompt asks if you want to use **lossless** WebP compression.
            *   **Lossless Compression ("yes"):**  Lossless compression preserves the *exact* original image data. This results in the highest possible quality WebP images, but they will generally be **larger** in file size than lossy WebP images. Lossless is best for images where perfect quality is absolutely critical and file size is less of a concern (e.g., archival purposes, certain types of illustrations).
            *   **Lossy Compression ("no" - Default):** Lossy compression reduces file size by discarding some image data that is generally not perceptually significant. This is usually the preferred method for web images as it achieves significant file size reductions while maintaining visually very good quality.
        *   **To use the default of lossy compression, simply press Enter without typing anything** (or type `no` and press Enter).
        *   **To enable lossless compression, type `yes` and press Enter.**
        *   **Press Enter** after typing `yes` or `no` (or just press Enter to use the default lossy compression).

*   **Example Interactive CLI Session:**

    Let's say you have a folder of images called `vacation_pics` in your `Pictures` directory, and you want to convert them to WebP, saving the WebP files in a new folder called `webp_vacation_pics` in the same `Pictures` directory, using the default quality and lossy compression.  Here's how a typical interactive session in your terminal would look:

    ```bash
    python webp_cli_converter.py
    Enter the path to the input folder containing images: /Users/yourusername/Pictures/vacation_pics
    Enter the path to the output folder (leave blank to save in input folder): /Users/yourusername/Pictures/webp_vacation_pics
    Enter WebP quality (0-100, default 80):  <-- Just press Enter here for default 80
    Use lossless WebP compression? (yes/no, default no):  <-- Just press Enter here for default 'no'

    Converting: image1.png to image1.webp
    Saved: image1.webp
    Converting: image2.jpg to image2.webp
    Saved: image2.webp
    ... (and so on for all images in the input folder) ...
    Conversion complete!
    ```

    After the script finishes, you'll find your converted WebP images in the `/Users/yourusername/Pictures/webp_vacation_pics` folder (or your equivalent paths).

*   **Status and Error Messages:** The script will print messages to your terminal as it converts each image, indicating the progress. If any errors occur during the conversion of a particular image, an error message will be displayed in the terminal, helping you diagnose any issues.


### 2. Graphical User Interface (GUI): For Visual Interaction and Ease of Use

The GUI provides a user-friendly, point-and-click interface for converting images. It's ideal for users who prefer visual interaction and a simpler workflow.

*   **Running the GUI Script:** Open your terminal or command prompt, navigate to your project directory, ensure your virtual environment is activated, and run the GUI script:

    ```bash
    python webp_converter_gui.py
    ```

    **Important:** `webp_converter_gui.py` is assumed to be the name of your GUI script file. Adjust the filename if necessary.

*   **Using the GUI:** Once the GUI application launches, you will typically see the following elements:

    *   **Input Folder Selection:** A button or field to browse and select the folder containing the PNG and JPG images you want to convert.
    *   **Output Folder Selection:** A button or field to choose the folder where the converted WebP images will be saved.
    *   **Quality Setting:** A slider or input field to adjust the WebP quality level.
    *   **Lossless Compression Checkbox:** An option to enable or disable lossless WebP compression.
    *   **Recursive Conversion Checkbox:** An option to process images in subfolders.
    *   **Convert Images Button:** A button to initiate the image conversion process.
    *   **Output/Status Area:** A text area to display status messages, progress updates, and any errors that occur during conversion.

*   **Step-by-Step GUI Workflow:**

    1.  **Select Input Folder:** Click the "Browse Input Folder" (or similar) button and choose the folder containing your PNG and JPG images.
    2.  **Select Output Folder:** Click the "Browse Output Folder" (or similar) button and choose the destination folder for the converted WebP images. If you don't specify an output folder, the WebP images might be saved in the same directory as the original images or in a default output location.
    3.  **Adjust Quality (Optional):** Use the quality slider or input field to set the desired WebP quality. A quality value between 75 and 90 is often a good balance between file size and visual quality. For maximum quality (at the expense of file size), use a higher value like 95 or 100.
    4.  **Enable Lossless Compression (Optional):** Check the "Lossless Compression" checkbox if you need to preserve the absolute best image quality and file size is less of a concern. Lossless WebP files will be larger than lossy WebP files.
    5.  **Enable Recursive Conversion (Optional):** Check the "Recursive Conversion" checkbox if you want to convert images in subfolders within the input folder as well.
    6.  **Click "Convert Images":** Press the "Convert Images" button to start the conversion process.
    7.  **Monitor Status:** Watch the output/status area for progress messages and any error notifications. The GUI will typically display messages indicating which images are being converted and when the process is complete.

*   **Post-Conversion:** Once the conversion is finished, check the output folder you specified. You should find the converted WebP images in that folder. The GUI might also provide a summary of the conversion process, such as the number of images converted and any errors encountered.

By following these setup and usage instructions, you should be well-equipped to efficiently convert your PNG and JPG images to WebP format using either the command-line or graphical interface of the Image to WebP Converter. Enjoy the benefits of reduced file sizes and optimized web performance!
