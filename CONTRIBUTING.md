# Contributing to Image to WebP Converter

First off, thank you for considering contributing to the Image to WebP Converter! We welcome any help to make this tool better. Whether it's reporting a bug, proposing a new feature, or writing code, your input is valuable.

This document provides guidelines for contributing. Please take a moment to review it.

## Table of Contents

*   [Code of Conduct](#code-of-conduct)
*   [How Can I Contribute?](#how-can-i-contribute)
    *   [Reporting Bugs](#reporting-bugs)
    *   [Suggesting Enhancements or Features](#suggesting-enhancements-or-features)
    *   [Your First Code Contribution](#your-first-code-contribution)
    *   [Pull Requests](#pull-requests)
*   [Development Setup](#development-setup)
*   [Style Guides](#style-guides)
    *   [Python Code](#python-code)
    *   [Commit Messages](#commit-messages)
*   [Questions?](#questions)

## Code of Conduct

This project and everyone participating in it is governed by our [Code of Conduct](CODE_OF_CONDUCT.md). By participating, you are expected to uphold this code. Please report unacceptable behavior. *(You'll need to create a CODE_OF_CONDUCT.md file - a common one is the Contributor Covenant).*

## How Can I Contribute?

### Reporting Bugs

Bugs are tracked as [GitHub Issues](https://github.com/Ktiseos-Nyx/Webp_Gui_Converter/issues). If you're not using GitHub Issues yet, you can report bugs in our [Discord server's](https://discord.gg/HhBSvM9gBY) appropriate channel.

Before reporting a bug, please check if it has already been reported.

When reporting a bug, please include:

1.  **A clear and descriptive title.**
2.  **Steps to reproduce the bug:** Be as specific as possible.
3.  **What you expected to happen.**
4.  **What actually happened.** Include screenshots if helpful.
5.  **Your operating system and version.**
6.  **The version of Python you are using.**
7.  **The version of the Image to WebP Converter (if applicable/versioned).**
8.  **Any error messages or stack traces.**

### Suggesting Enhancements or Features

We love to hear your ideas for making the converter even better!

1.  **Check existing suggestions:** Before submitting, see if your idea has already been proposed [on GitHub Issues](link-to-your-github-issues-page) or discussed on [Discord](https://discord.gg/HhBSvM9gBY).
2.  **Provide a clear description:** Explain the enhancement or feature, why it would be useful, and if possible, how you envision it working.

### Your First Code Contribution

Unsure where to begin contributing code?
*   Look for issues tagged `good first issue` or `help wanted` on our [GitHub Issues page](link-to-your-github-issues-page) (once set up).
*   You can also ask on our [Discord server](https://discord.gg/HhBSvM9gBY) for good starting points.

### Pull Requests

If you've written code to fix a bug or implement a feature:

1.  **Fork the repository** (if on GitHub).
2.  **Create a new branch** for your changes: `git checkout -b feature/your-feature-name` or `bugfix/issue-number-description`.
3.  **Make your changes.**
4.  **Add tests** for your changes, if applicable.
5.  **Ensure your code lints** and follows the style guide (see [Style Guides](#style-guides)).
6.  **Write clear commit messages** (see [Commit Messages](#commit-messages)).
7.  **Push your branch** to your fork.
8.  **Open a Pull Request (PR)** against the `main` (or `develop`) branch of the original repository.
    *   Provide a clear title and description for your PR, explaining the changes and referencing any related issues (e.g., "Fixes #123").

*(If you are not using GitHub yet, you can share your code changes as a patch file or via a shared code snippet on Discord for review.)*

## Development Setup

To set up the project for local development:

1.  **Clone the repository:**
    ```bash
    git clone [URL_of_your_repository]
    cd Image-to-WebP-Converter # Or your repository name
    ```
    *(If not using Git, download the source code as a ZIP and extract it.)*

2.  **Create and activate a virtual environment:**
    ```bash
    python3 -m venv .venv
    source .venv/bin/activate  # macOS/Linux
    # .venv\Scripts\activate.bat # Windows CMD
    # .venv\Scripts\Activate.ps1 # Windows PowerShell
    ```

3.  **Install dependencies (including development tools if any):**
    ```bash
    pip install Pillow PyQt6 qt-material
    # pip install -r requirements_dev.txt # If you create a dev requirements file
    ```
    We recommend also installing linters/formatters like `flake8` and `black`:
    ```bash
    pip install flake8 black
    ```

## Style Guides

### Python Code

*   Follow **PEP 8** - Style Guide for Python Code.
*   We use **Black** for code formatting. Before committing, you can format your code:
    ```bash
    black .
    ```
*   We use **Flake8** for linting. Check for issues:
    ```bash
    flake8 .
    ```
*   Keep lines under a reasonable length (e.g., 99 characters, configurable with Black).
*   Write clear, readable code with comments where necessary.

### Commit Messages

*   Use the present tense ("Add feature" not "Added feature").
*   Use the imperative mood ("Fix bug" not "Fixes bug" or "Fixed bug").
*   Limit the first line to 72 characters or less.
*   Reference issues and pull requests liberally after the first line.
*   Consider using [Conventional Commits](https://www.conventionalcommits.org/) for a more structured history, e.g.:
    *   `feat: Add lossless compression option to GUI`
    *   `fix: Prevent crash when input folder is empty`
    *   `docs: Update README with installation instructions`
    *   `style: Format code with Black`
    *   `refactor: Improve efficiency of image processing loop`
    *   `test: Add unit tests for conversion logic`

## Questions?

If you have any questions, feel free to ask on our [Discord server](https://discord.gg/HhBSvM9gBY) or [open an issue](link-to-your-github-issues-page).

Thank you for contributing!
