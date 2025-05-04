import sys
import os
from PyQt6.QtWidgets import (QApplication, QMainWindow, QLabel, QLineEdit,
                             QPushButton, QVBoxLayout, QHBoxLayout, QWidget,
                             QFileDialog, QSpinBox, QCheckBox, QTextEdit,
                             QMessageBox, QProgressBar)
from PyQt6.QtCore import Qt
from PIL import Image

class ImageConverterGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Image to WebP Converter")
        self.setGeometry(100, 100, 600, 500)  # Increased height for progress bar

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

        self.output_folder_layout = QHBoxLayout() # To be enabled/disabled
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
        self.quality_spinbox.setValue(80) # Default quality
        webp_settings_layout.addWidget(self.quality_label)
        webp_settings_layout.addWidget(self.quality_spinbox)
        self.layout.addLayout(webp_settings_layout)

        lossless_layout = QHBoxLayout()
        self.lossless_checkbox = QCheckBox("Lossless Compression")
        lossless_layout.addWidget(self.lossless_checkbox)
        lossless_layout.addStretch(1) # Push to the left
        self.layout.addLayout(lossless_layout)

        # --- Progress Bar ---
        self.progress_bar = QProgressBar()
        self.layout.addWidget(self.progress_bar)

        # --- Convert Button ---
        self.convert_button = QPushButton("Convert Images")
        self.convert_button.clicked.connect(self.start_conversion)
        self.layout.addWidget(self.convert_button)

        # --- Status Output ---
        self.status_output = QTextEdit()
        self.status_output.setReadOnly(True) # Make it read-only for status display
        self.layout.addWidget(self.status_output)

        # --- Initialization ---
        self.toggle_output_folder_widgets(Qt.CheckState.Unchecked) # Initially hide output folder widgets

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
        input_folder = self.input_folder_line_edit.text()
        output_folder = self.output_folder_line_edit.text() if self.output_folder_checkbox.isChecked() else None
        quality = self.quality_spinbox.value()
        lossless = self.lossless_checkbox.isChecked()

        if not input_folder:
            QMessageBox.warning(self, "Input Folder Missing", "Please select an input folder.")
            return

        if not os.path.isdir(input_folder):
            QMessageBox.warning(self, "Invalid Input Folder", "The specified input folder is not valid.")
            return

        if self.output_folder_checkbox.isChecked() and not output_folder:
            QMessageBox.warning(self, "Output Folder Missing", "Please select an output folder.")
            return

        if self.output_folder_checkbox.isChecked() and not os.path.isdir(output_folder):
             QMessageBox.warning(self, "Invalid Output Folder", "The specified output folder is not valid.")
             return


        self.status_output.clear() # Clear previous status
        self.status_output.append("Starting conversion...")
        self.convert_button.setEnabled(False) # Disable button during conversion
        self.progress_bar.setValue(0) # Reset progress bar

        try:
            self.convert_images_to_webp(input_folder, output_folder, quality, lossless) # Call the conversion function
            self.status_output.append("Conversion complete!")
        except Exception as e:
            self.status_output.append(f"An error occurred: {e}")
            QMessageBox.critical(self, "Error", f"Conversion failed. See status output for details.\nError: {e}") # Display error dialog
        finally:
            self.convert_button.setEnabled(True) # Re-enable button after conversion (or error)
            self.progress_bar.setValue(0) # Reset progress bar


    def convert_images_to_webp(self, input_folder, output_folder, quality, lossless):
        """
        Converts images in the input folder to WebP format, saving them in the specified output folder.
        """
        if output_folder is None:
            output_folder = input_folder

        if not os.path.exists(output_folder):
            os.makedirs(output_folder, exist_ok=True)

        # Create a set of valid image extensions for faster checking
        valid_extensions = {'.png', '.jpg', '.jpeg'}
        image_files = [f for f in os.listdir(input_folder) if os.path.isfile(os.path.join(input_folder, f)) and os.path.splitext(f.lower())[1] in valid_extensions]
        num_images = len(image_files)
        if num_images == 0:
            self.status_output.append("No PNG or JPG images found in the input folder.")
            QMessageBox.information(self, "No Images Found", "No PNG or JPG images were found in the selected input folder.")
            return

        self.progress_bar.setRange(0, num_images)
        converted_count = 0

        for filename in image_files:
            input_filepath = os.path.join(input_folder, filename)
            try:
                try:
                    img = Image.open(input_filepath)
                except Exception as e:
                    error_message = f"Error opening {filename}: {e}"
                    self.status_output.append(error_message)
                    QApplication.processEvents()
                    continue  # Skip to the next image

                base_filename, ext = os.path.splitext(filename)
                output_webp_filename = base_filename + ".webp"
                output_webp_filepath = os.path.join(output_folder, output_webp_filename)

                status_message = f"Converting: {filename} to {output_webp_filename}"
                self.status_output.append(status_message)
                QApplication.processEvents() # Important: Update GUI during long process

                img.save(output_webp_filepath, 'webp', quality=quality, lossless=lossless)

                status_message = f"Saved: {output_webp_filename}"
                self.status_output.append(status_message)
                QApplication.processEvents() # Update GUI again

            except Exception as e:
                error_message = f"Error processing {filename}: {e}"
                self.status_output.append(error_message)
                QApplication.processEvents() # Update GUI with error message
            finally:
                converted_count += 1
                self.progress_bar.setValue(converted_count)
                QApplication.processEvents()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ImageConverterGUI()
    window.show()
    sys.exit(app.exec())
