import sys
import os
from PyQt6.QtWidgets import (QApplication, QMainWindow, QLabel, QLineEdit,
                             QPushButton, QVBoxLayout, QHBoxLayout, QWidget,
                             QFileDialog, QSpinBox, QCheckBox, QTextEdit,
                             QMessageBox, QProgressBar)
from PyQt6.QtCore import Qt, QThread, pyqtSignal
import image_converter  # Import the shared module

class ConversionThread(QThread):
    """A QThread to handle the image conversion process in the background."""
    progress_update = pyqtSignal(int, int, str)  # Signal for progress updates
    finished_signal = pyqtSignal() # Signal when conversion is complete
    error_signal = pyqtSignal(str) # Signal for error messages

    def __init__(self, input_path, output_dir, quality, lossless, recursive, no_overwrite):
        super().__init__()
        self.input_path = input_path
        self.output_dir = output_dir
        self.quality = quality
        self.lossless = lossless
        self.recursive = recursive
        self.no_overwrite = no_overwrite

    def run(self):
        """Runs the image conversion process."""
        try:
            image_converter.process_images(
                self.input_path, self.output_dir, self.quality, self.lossless,
                self.recursive, self.no_overwrite, self.progress_update.emit  # Pass callback
            )
            self.finished_signal.emit()
        except Exception as e:
            self.error_signal.emit(str(e))


class ImageConverterGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Image to WebP Converter")
        self.setGeometry(100, 100, 600, 500)

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

    def toggle_output_folder_widgets(self, state):
        enabled = (state == Qt.CheckState.Checked)
        self.output_folder_label.setEnabled(enabled)
        self.output_folder_line_edit.setEnabled(enabled)
        self.output_folder_button.setEnabled(enabled)

    def start_conversion(self):
        input_path = self.input_folder_line_edit.text()
        output_dir = self.output_folder_line_edit.text() if self.output_folder_checkbox.isChecked() else None
        quality = self.quality_spinbox.value()
        lossless = self.lossless_checkbox.isChecked()
        recursive = self.recursive_checkbox.isChecked()
        no_overwrite = not self.overwrite_checkbox.isChecked() # Invert the logic
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
            QMessageBox.warning(self, "Output Missing", "Please select an output folder.")
            self.convert_button.setEnabled(True)
            return

        # Create and start the conversion thread
        self.conversion_thread = ConversionThread(input_path, output_dir, quality, lossless, recursive, no_overwrite)
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

    def conversion_complete(self):
        """Called when the conversion thread finishes successfully."""
        self.status_output.append("Conversion complete!")
        self.convert_button.setEnabled(True)

    def conversion_error(self, message):
        """Called when the conversion thread encounters an error."""
        self.status_output.append(f"Error: {message}")
        QMessageBox.critical(self, "Error", f"Conversion failed: {message}")
        self.convert_button.setEnabled(True)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ImageConverterGUI()
    window.show()
    sys.exit(app.exec())
