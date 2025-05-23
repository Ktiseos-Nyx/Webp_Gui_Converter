import sys
import os
import zipfile
from PyQt6.QtWidgets import (QApplication, QMainWindow, QLabel, QLineEdit,
                             QPushButton, QVBoxLayout, QHBoxLayout, QWidget,
                             QFileDialog, QSpinBox, QCheckBox, QTextEdit,
                             QMessageBox, QProgressBar, QDialog,
                             QDialogButtonBox)
from PyQt6.QtCore import Qt, QThread, pyqtSignal

# --- Added for Qt Material ---
try:
    import qt_material
except ImportError:
    print("qt-material library not found. Please install it: pip install qt-material")
    qt_material = None
# -----------------------------

import image_converter  # Import the shared module

class NewFolderDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Create New Folder")

        self.layout = QVBoxLayout()
        self.label = QLabel("Folder Name:")
        self.lineEdit = QLineEdit()
        self.layout.addWidget(self.label)
        self.layout.addWidget(self.lineEdit)

        self.buttonBox = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)
        self.layout.addWidget(self.buttonBox)

        self.setLayout(self.layout)

    def getFolderName(self):
        return self.lineEdit.text()

class ConversionThread(QThread):
    """A QThread to handle the image conversion process in the background."""
    progress_update = pyqtSignal(int, int, str)  # Signal for progress updates
    finished_signal = pyqtSignal(str) # Signal when conversion is complete (pass output folder)
    error_signal = pyqtSignal(str) # Signal for error messages

    def __init__(self, input_path, output_dir, quality, lossless, recursive, no_overwrite, zip_output):
        super().__init__()
        self.input_path = input_path
        self.output_dir = output_dir
        self.quality = quality
        self.lossless = lossless
        self.recursive = recursive
        self.no_overwrite = no_overwrite
        self.zip_output = zip_output

    def run(self):
        """Runs the image conversion process."""
        try:
            image_converter.process_images(
                self.input_path, self.output_dir, self.quality, self.lossless,
                self.recursive, self.no_overwrite, self.progress_update.emit  # Pass callback
            )
            self.finished_signal.emit(self.output_dir)  # Pass output folder to finished signal
        except Exception as e:
            self.error_signal.emit(str(e))


class ImageConverterGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Image to WebP Converter")

        # --- 1. Window Size Rules ---
        # Set a fixed size. This ensures consistency across different OS/screen sizes.
        # We'll use 600 width (as before) and increase height a bit for better spacing.
        # This meets your minimum 500x600 requirement.
        self.setFixedSize(600, 650)
        # You can also set initial position if you like:
        # self.move(100, 100) # Or use QScreen to center it

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)

        # --- Input Folder ---
        input_folder_layout = QHBoxLayout()
        self.input_folder_label = QLabel("Input Folder:")
        self.input_folder_line_edit = QLineEdit()
        self.input_folder_button = QPushButton("Browse Input...")
        self.input_folder_button.clicked.connect(self.browse_input_folder)
        input_folder_layout.addWidget(self.input_folder_label)
        input_folder_layout.addWidget(self.input_folder_line_edit)
        input_folder_layout.addWidget(self.input_folder_button)
        self.layout.addLayout(input_folder_layout)

        # --- Output Folder ---
        self.output_folder_checkbox = QCheckBox("Use Separate Output Folder")
        self.output_folder_checkbox.stateChanged.connect(self.toggle_output_folder_widgets)
        self.layout.addWidget(self.output_folder_checkbox)

        self.output_folder_layout = QHBoxLayout()
        self.output_folder_label = QLabel("Output Folder:")
        self.output_folder_line_edit = QLineEdit()
        self.output_folder_button = QPushButton("Browse Output...")
        self.output_folder_button.clicked.connect(self.browse_output_folder)
        self.output_folder_layout.addWidget(self.output_folder_label)
        self.output_folder_layout.addWidget(self.output_folder_line_edit)
        self.output_folder_layout.addWidget(self.output_folder_button)
        self.layout.addLayout(self.output_folder_layout)

        # --- Create Output Folder Button ---
        self.create_output_folder_button = QPushButton("Create New Output Folder...")
        self.create_output_folder_button.clicked.connect(self.create_output_folder)
        self.layout.addWidget(self.create_output_folder_button)

        self.output_folder_hint_label = QLabel("(If unchecked, WebP saved in input folder)")
        self.output_folder_hint_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.output_folder_hint_label)

        # --- WebP Settings ---
        webp_settings_layout = QHBoxLayout()
        self.quality_label = QLabel("WebP Quality (0-100):")
        self.quality_spinbox = QSpinBox()
        self.quality_spinbox.setRange(0, 100)
        self.quality_spinbox.setValue(80)
        webp_settings_layout.addWidget(self.quality_label)
        webp_settings_layout.addWidget(self.quality_spinbox)
        self.layout.addLayout(webp_settings_layout)

        lossless_layout = QHBoxLayout()
        self.lossless_checkbox = QCheckBox("Lossless Compression")
        lossless_layout.addWidget(self.lossless_checkbox)
        lossless_layout.addStretch(1)
        self.layout.addLayout(lossless_layout)

        # --- Recursive Checkbox ---
        self.recursive_checkbox = QCheckBox("Process Subfolders Recursively")
        self.layout.addWidget(self.recursive_checkbox)

        # --- Overwrite Checkbox ---
        self.overwrite_checkbox = QCheckBox("Overwrite Existing Files")
        self.overwrite_checkbox.setChecked(True) # Default to overwrite
        self.layout.addWidget(self.overwrite_checkbox)

        # --- Zip Output Checkbox ---
        self.zip_output_checkbox = QCheckBox("Zip Output Folder After Conversion")
        self.layout.addWidget(self.zip_output_checkbox)

        # --- Progress Bar ---
        self.progress_bar = QProgressBar()
        self.layout.addWidget(self.progress_bar)

        # --- Convert Button ---
        self.convert_button = QPushButton("Convert Images")
        self.convert_button.clicked.connect(self.start_conversion)
        self.layout.addWidget(self.convert_button)

        # --- Status Output ---
        self.status_output = QTextEdit()
        self.status_output.setReadOnly(True)
        self.layout.addWidget(self.status_output)

        # --- Initialization ---
        self.toggle_output_folder_widgets(Qt.CheckState.Unchecked.value) # Pass the integer value

    def browse_input_folder(self):
        folder_path = QFileDialog.getExistingDirectory(self, "Select Input Folder")
        if folder_path:
            self.input_folder_line_edit.setText(folder_path)

    def browse_output_folder(self):
        folder_path = QFileDialog.getExistingDirectory(self, "Select Output Folder")
        if folder_path:
            self.output_folder_line_edit.setText(folder_path)

    def create_output_folder(self):
        """Creates a new output folder using a custom dialog."""
        input_folder = self.input_folder_line_edit.text()
        if not input_folder and not self.output_folder_line_edit.text():
             # Allow creating if output parent is already selected
            parent_dir_for_new_folder = QFileDialog.getExistingDirectory(self, "Select Parent Folder for New Output Folder")
            if not parent_dir_for_new_folder:
                return # User cancelled
        elif self.output_folder_line_edit.text() and os.path.isdir(self.output_folder_line_edit.text()):
            parent_dir_for_new_folder = self.output_folder_line_edit.text()
        elif input_folder and os.path.isdir(input_folder):
            parent_dir_for_new_folder = input_folder # Default to input folder if nothing else
        else:
            QMessageBox.warning(self, "Base Folder Missing", "Please select an input folder or an existing output folder to create a subfolder in.")
            return

        dialog = NewFolderDialog(self)
        result = dialog.exec()

        if result == QDialog.DialogCode.Accepted:
            folder_name = dialog.getFolderName()
            if not folder_name:
                QMessageBox.warning(self, "Folder Name Missing", "Please enter a folder name.")
                return

            new_folder_path = os.path.join(parent_dir_for_new_folder, folder_name)
            try:
                os.makedirs(new_folder_path, exist_ok=True) # exist_ok=True is safer
                self.output_folder_line_edit.setText(new_folder_path)
                self.output_folder_checkbox.setChecked(True)
            except OSError as e:
                QMessageBox.critical(self, "Error Creating Folder", f"Could not create folder: {e}")

    def toggle_output_folder_widgets(self, state_value): # state_value is int
        # The stateChanged signal for QCheckBox emits an int (the value of Qt.CheckState)
        enabled = (state_value == Qt.CheckState.Checked.value)
        # Alternatively, you could just check the checkbox's current state:
        # enabled = self.output_folder_checkbox.isChecked()

        self.output_folder_label.setEnabled(enabled)
        self.output_folder_line_edit.setEnabled(enabled)
        self.output_folder_button.setEnabled(enabled)
        # Keep create output folder button always enabled or also tied to this?
        # For now, let's tie it to the checkbox, implying it's for creating *the* separate output folder.
        self.create_output_folder_button.setEnabled(enabled)
        self.output_folder_hint_label.setText(
            "(If unchecked, WebP saved in input folder)" if not enabled
            else "(WebP will be saved in the specified output folder)"
        )


    def start_conversion(self):
        input_path = self.input_folder_line_edit.text()
        output_dir = self.output_folder_line_edit.text() if self.output_folder_checkbox.isChecked() else None
        quality = self.quality_spinbox.value()
        lossless = self.lossless_checkbox.isChecked()
        recursive = self.recursive_checkbox.isChecked()
        no_overwrite = not self.overwrite_checkbox.isChecked() # Invert the logic
        zip_output = self.zip_output_checkbox.isChecked()

        # Disable button during conversion
        self.convert_button.setEnabled(False)
        self.progress_bar.setValue(0)
        self.status_output.clear()

        # Input Validation
        if not input_path:
            QMessageBox.warning(self, "Input Missing", "Please select an input folder or file.")
            self.convert_button.setEnabled(True)
            return

        if self.output_folder_checkbox.isChecked() and not output_dir:
            QMessageBox.warning(self, "Output Missing", "Please specify an output folder or uncheck 'Use Separate Output Folder'.")
            self.convert_button.setEnabled(True)
            return

        # Create and start the conversion thread
        self.conversion_thread = ConversionThread(input_path, output_dir, quality, lossless, recursive, no_overwrite, zip_output)
        self.conversion_thread.progress_update.connect(self.update_progress)
        self.conversion_thread.finished_signal.connect(self.conversion_complete)
        self.conversion_thread.error_signal.connect(self.conversion_error)
        self.conversion_thread.start()

    def update_progress(self, current, total, message):
        """Updates the progress bar and status output."""
        if total > 0 : # Avoid division by zero if total is somehow 0 initially
            self.progress_bar.setMaximum(total)
            self.progress_bar.setValue(current)
        else:
            self.progress_bar.setMaximum(1) #indeterminate
            self.progress_bar.setValue(0)
        self.status_output.append(message)
        QApplication.processEvents() # Keep GUI responsive

    def conversion_complete(self, output_dir_used): # output_dir_used can be None
        """Called when the conversion thread finishes successfully."""
        self.status_output.append("Conversion complete!")
        final_output_dir = output_dir_used
        if not final_output_dir: # If output_dir was None, it means input_path was used
            final_output_dir = self.input_folder_line_edit.text()
            if os.path.isfile(final_output_dir): # if input was a file, get its directory
                final_output_dir = os.path.dirname(final_output_dir)


        if self.zip_output_checkbox.isChecked() and final_output_dir:
            try:
                # Determine zip filename based on the actual output directory
                zip_filename = os.path.basename(os.path.normpath(final_output_dir)) + ".zip"
                # Place zip file in the parent of the final_output_dir
                zip_filepath = os.path.join(os.path.dirname(final_output_dir), zip_filename)

                self.status_output.append(f"Zipping folder: {final_output_dir} to {zip_filepath}")
                self.zip_folder(final_output_dir, zip_filepath)
                self.status_output.append(f"Zipped output to: {zip_filepath}")
                QMessageBox.information(self, "Zipping Complete", f"Output folder zipped to {zip_filepath}")

            except Exception as e:
                self.status_output.append(f"Error zipping output: {e}")
                QMessageBox.critical(self, "Error Zipping", f"Could not zip output folder: {e}")
        self.convert_button.setEnabled(True)

    def conversion_error(self, message):
        """Called when the conversion thread encounters an error."""
        self.status_output.append(f"Error: {message}")
        QMessageBox.critical(self, "Error", f"Conversion failed: {message}")
        self.convert_button.setEnabled(True)

    def zip_folder(self, folder_path, zip_path):
        """Zips the contents of a folder to a zip file."""
        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, _, files in os.walk(folder_path):
                for file in files:
                    file_path = os.path.join(root, file)
                    # Add file to zip, using relative path inside the zip
                    zipf.write(file_path, os.path.relpath(file_path, os.path.join(folder_path, '..')))


if __name__ == "__main__":
    app = QApplication(sys.argv)

    # --- 2. Implement Qt Material themes ---
    if qt_material:
        # Apply a theme. You can try different themes:
        # 'dark_teal.xml', 'light_blue.xml', 'dark_red.xml', etc.
        # List available themes: print(qt_material.list_themes())
        try:
            qt_material.apply_stylesheet(app, theme='dark_blue.xml')
        except Exception as e:
            print(f"Could not apply qt-material theme: {e}")
    else:
        print("Skipping Qt Material theme application.")
    # ------------------------------------

    window = ImageConverterGUI()
    window.show()
    sys.exit(app.exec())
