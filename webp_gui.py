import sys
import os
import zipfile
from PyQt6.QtWidgets import (QApplication, QMainWindow, QLabel, QLineEdit,
                             QPushButton, QVBoxLayout, QHBoxLayout, QWidget,
                             QFileDialog, QSpinBox, QCheckBox, QTextEdit,
                             QMessageBox, QProgressBar, QInputDialog, QDialog,
                             QDialogButtonBox)
from PyQt6.QtCore import Qt, QThread, pyqtSignal

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
        self.setGeometry(100, 100, 600, 550) # Increased height

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
        self.toggle_output_folder_widgets(Qt.CheckState.Unchecked)

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
        if not input_folder:
            QMessageBox.warning(self, "Input Folder Missing", "Please select an input folder first.")
            return

        output_folder = QFileDialog.getExistingDirectory(self, "Select Parent Folder for New Output Folder")
        if not output_folder:
            return  # User cancelled

        dialog = NewFolderDialog(self)
        result = dialog.exec()

        if result == QDialog.DialogCode.Accepted:
            folder_name = dialog.getFolderName()
            if not folder_name:
                QMessageBox.warning(self, "Folder Name Missing", "Please enter a folder name.")
                return

            new_folder_path = os.path.join(output_folder, folder_name)
            try:
                os.makedirs(new_folder_path)
                self.output_folder_line_edit.setText(new_folder_path)
                self.output_folder_checkbox.setChecked(True)  # Automatically check the box
                print("Checkbox checked programmatically!")
            except OSError as e:
                QMessageBox.critical(self, "Error Creating Folder", f"Could not create folder: {e}")

    def toggle_output_folder_widgets(self, state):
        print(f"toggle_output_folder_widgets called with state: {state}")
        enabled = (state == Qt.CheckState.Checked.value)
        print(f"Enabled: {enabled}")
        self.output_folder_label.setEnabled(enabled)
        self.output_folder_line_edit.setEnabled(enabled)
        self.output_folder_button.setEnabled(enabled)
        self.create_output_folder_button.setEnabled(enabled)

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

        # Create and start the conversion thread
        self.conversion_thread = ConversionThread(input_path, output_dir, quality, lossless, recursive, no_overwrite, zip_output)
        self.conversion_thread.progress_update.connect(self.update_progress)
        self.conversion_thread.finished_signal.connect(self.conversion_complete)
        self.conversion_thread.error_signal.connect(self.conversion_error)
        self.conversion_thread.start()

    def update_progress(self, current, total, message):
        """Updates the progress bar and status output."""
        self.progress_bar.setMaximum(total)
        self.progress_bar.setValue(current)
        self.status_output.append(message)
        QApplication.processEvents() # Keep GUI responsive

    def conversion_complete(self, output_dir):
        """Called when the conversion thread finishes successfully."""
        self.status_output.append("Conversion complete!")
        if self.zip_output_checkbox.isChecked():
            try:
                zip_filename = os.path.basename(output_dir) + ".zip"
                zip_filepath = os.path.join(os.path.dirname(output_dir), zip_filename)
                self.zip_folder(output_dir, zip_filepath)
                self.status_output.append(f"Zipped output to: {zip_filename}")
                QMessageBox.information(self, "Zipping Complete", f"Output folder zipped to {zip_filename}")

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
                    zipf.write(file_path, os.path.relpath(file_path, folder_path))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ImageConverterGUI()
    window.show()
    sys.exit(app.exec())
