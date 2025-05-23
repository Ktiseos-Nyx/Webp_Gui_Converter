import sys
import os
import zipfile
from functools import partial # Added for connecting menu actions

from PyQt6.QtWidgets import (QApplication, QMainWindow, QLabel, QLineEdit,
                             QPushButton, QVBoxLayout, QHBoxLayout, QWidget,
                             QFileDialog, QSpinBox, QCheckBox, QTextEdit,
                             QMessageBox, QProgressBar, QDialog,
                             QDialogButtonBox)
from PyQt6.QtGui import QAction # Added for menu actions
from PyQt6.QtCore import Qt, QThread, pyqtSignal

# --- Added for Qt Material ---
try:
    import qt_material
except ImportError:
    print("qt-material library not found. Please install it: pip install qt-material")
    qt_material = None
# -----------------------------

# --- Placeholder for your image_converter module ---
# Create a dummy image_converter.py in the same directory for this to run without errors
# if you don't have the actual one. Example dummy:
# def process_images(input_path, output_dir, quality, lossless, recursive, no_overwrite, progress_callback):
#     print(f"Simulating processing: {input_path} to {output_dir}")
#     progress_callback(1, 1, "Done simulation")
#     pass
import image_converter  # Import the shared module
# -------------------------------------------------

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
            # Ensure image_converter.process_images exists and takes these arguments
            image_converter.process_images(
                self.input_path, self.output_dir, self.quality, self.lossless,
                self.recursive, self.no_overwrite, self.progress_update.emit  # Pass callback
            )
            self.finished_signal.emit(self.output_dir)  # Pass output folder to finished signal
        except Exception as e:
            self.error_signal.emit(str(e))


class ImageConverterGUI(QMainWindow):
    # Define standard sizes as a class attribute for easy access
    PREDEFINED_SIZES = {
        "Default (600x650)": (600, 650),
        "Portrait - Tall (600x800)": (600, 800),
        "Square - Small (700x700)": (700, 700),
        "Landscape - Small (800x600)": (800, 600),
        "Landscape - Medium (1024x768)": (1024, 768),
    }
    DEFAULT_SIZE_NAME = "Default (600x650)"

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Image to WebP Converter")

        # Set initial fixed size using the default
        initial_width, initial_height = self.PREDEFINED_SIZES[self.DEFAULT_SIZE_NAME]
        self.setFixedSize(initial_width, initial_height)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)

        # --- Create Menu Bar for Size Options ---
        self._create_menu_bar()

        # --- UI Elements ---
        # Input Folder
        input_folder_layout = QHBoxLayout()
        self.input_folder_label = QLabel("Input Folder:")
        self.input_folder_line_edit = QLineEdit()
        self.input_folder_button = QPushButton("Browse Input...")
        self.input_folder_button.clicked.connect(self.browse_input_folder)
        input_folder_layout.addWidget(self.input_folder_label)
        input_folder_layout.addWidget(self.input_folder_line_edit)
        input_folder_layout.addWidget(self.input_folder_button)
        self.layout.addLayout(input_folder_layout)

        # Output Folder Checkbox
        self.output_folder_checkbox = QCheckBox("Use Separate Output Folder")
        self.output_folder_checkbox.stateChanged.connect(self.toggle_output_folder_widgets)
        self.layout.addWidget(self.output_folder_checkbox)

        # Output Folder Path
        self.output_folder_layout = QHBoxLayout()
        self.output_folder_label = QLabel("Output Folder:")
        self.output_folder_line_edit = QLineEdit()
        self.output_folder_button = QPushButton("Browse Output...")
        self.output_folder_button.clicked.connect(self.browse_output_folder)
        self.output_folder_layout.addWidget(self.output_folder_label)
        self.output_folder_layout.addWidget(self.output_folder_line_edit)
        self.output_folder_layout.addWidget(self.output_folder_button)
        self.layout.addLayout(self.output_folder_layout)

        # Create Output Folder Button
        self.create_output_folder_button = QPushButton("Create New Output Folder...")
        self.create_output_folder_button.clicked.connect(self.create_output_folder)
        self.layout.addWidget(self.create_output_folder_button)

        self.output_folder_hint_label = QLabel("(If unchecked, WebP saved in input folder)")
        self.output_folder_hint_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.output_folder_hint_label)

        # WebP Settings
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

        self.recursive_checkbox = QCheckBox("Process Subfolders Recursively")
        self.layout.addWidget(self.recursive_checkbox)

        self.overwrite_checkbox = QCheckBox("Overwrite Existing Files")
        self.overwrite_checkbox.setChecked(True)
        self.layout.addWidget(self.overwrite_checkbox)

        self.zip_output_checkbox = QCheckBox("Zip Output Folder After Conversion")
        self.layout.addWidget(self.zip_output_checkbox)

        self.progress_bar = QProgressBar()
        self.layout.addWidget(self.progress_bar)

        self.convert_button = QPushButton("Convert Images")
        self.convert_button.clicked.connect(self.start_conversion)
        self.layout.addWidget(self.convert_button)

        self.status_output = QTextEdit()
        self.status_output.setReadOnly(True)
        self.layout.addWidget(self.status_output)

        # Initialize widget states
        self.toggle_output_folder_widgets(Qt.CheckState.Unchecked.value)

    def _create_menu_bar(self):
        menu_bar = self.menuBar()
        view_menu = menu_bar.addMenu("&View")

        size_menu = view_menu.addMenu("Set Window &Size")

        for name, (width, height) in self.PREDEFINED_SIZES.items():
            action = QAction(name, self)
            action.triggered.connect(partial(self._set_selected_window_size, width, height))
            size_menu.addAction(action)

    def _set_selected_window_size(self, width, height):
        self.setFixedSize(width, height)
        # Optionally, save this preference if you implement settings persistence later

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
        parent_dir_for_new_folder = ""

        # Prefer existing output folder path as parent
        if self.output_folder_line_edit.text() and os.path.isdir(self.output_folder_line_edit.text()):
            parent_dir_for_new_folder = self.output_folder_line_edit.text()
        # Fallback to input folder path as parent
        elif self.input_folder_line_edit.text() and os.path.isdir(self.input_folder_line_edit.text()):
             parent_dir_for_new_folder = self.input_folder_line_edit.text()

        # If neither is set and valid, prompt user for a parent directory
        if not parent_dir_for_new_folder:
            selected_parent_dir = QFileDialog.getExistingDirectory(self, "Select Parent Folder for New Output Folder")
            if not selected_parent_dir:
                return # User cancelled
            parent_dir_for_new_folder = selected_parent_dir
        
        dialog = NewFolderDialog(self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            folder_name = dialog.getFolderName()
            if not folder_name:
                QMessageBox.warning(self, "Folder Name Missing", "Please enter a folder name.")
                return
            
            new_folder_path = os.path.join(parent_dir_for_new_folder, folder_name)
            try:
                os.makedirs(new_folder_path, exist_ok=True) # exist_ok=True prevents error if folder already exists
                self.output_folder_line_edit.setText(new_folder_path)
                # If we created an output folder, assume user wants to use it
                self.output_folder_checkbox.setChecked(True) 
            except OSError as e:
                QMessageBox.critical(self, "Error Creating Folder", f"Could not create folder: {e}")

    def toggle_output_folder_widgets(self, state_value): # state_value is int
        enabled = (state_value == Qt.CheckState.Checked.value)
        
        self.output_folder_label.setEnabled(enabled)
        self.output_folder_line_edit.setEnabled(enabled)
        self.output_folder_button.setEnabled(enabled)
        # The "Create New Output Folder" button is now also tied to this checkbox
        # to make it clear it's for creating the *separate* output folder.
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
        no_overwrite = not self.overwrite_checkbox.isChecked()
        zip_output = self.zip_output_checkbox.isChecked()

        self.convert_button.setEnabled(False)
        self.progress_bar.setValue(0)
        self.status_output.clear()

        if not input_path:
            QMessageBox.warning(self, "Input Missing", "Please select an input folder or file.")
            self.convert_button.setEnabled(True)
            return
        
        if self.output_folder_checkbox.isChecked() and not output_dir:
            QMessageBox.warning(self, "Output Missing", "Please specify an output folder or uncheck 'Use Separate Output Folder'.")
            self.convert_button.setEnabled(True)
            return
        
        # If a separate output folder is specified, ensure it exists or can be created
        if output_dir:
            if not os.path.isdir(output_dir):
                try:
                    os.makedirs(output_dir, exist_ok=True)
                    self.status_output.append(f"Created output directory: {output_dir}")
                except OSError as e:
                    QMessageBox.critical(self, "Output Directory Error", f"Could not create output directory '{output_dir}': {e}")
                    self.convert_button.setEnabled(True)
                    return

        self.conversion_thread = ConversionThread(input_path, output_dir, quality, lossless, recursive, no_overwrite, zip_output)
        self.conversion_thread.progress_update.connect(self.update_progress)
        self.conversion_thread.finished_signal.connect(self.conversion_complete)
        self.conversion_thread.error_signal.connect(self.conversion_error)
        self.conversion_thread.start()

    def update_progress(self, current, total, message):
        if total > 0 :
            self.progress_bar.setMaximum(total)
            self.progress_bar.setValue(current)
        else: # Handle indeterminate case or initial state
            self.progress_bar.setMaximum(100) # or 0 for busy indicator style
            self.progress_bar.setValue(0)
        self.status_output.append(message)
        QApplication.processEvents()

    def conversion_complete(self, output_dir_from_thread):
        self.status_output.append("Conversion complete!")
        
        # Determine the actual directory where files were outputted
        final_output_dir = ""
        if output_dir_from_thread: # A separate output directory was used
            final_output_dir = output_dir_from_thread
        else: # Output was in the input directory
            input_path_text = self.input_folder_line_edit.text()
            if os.path.isdir(input_path_text):
                final_output_dir = input_path_text
            elif os.path.isfile(input_path_text):
                final_output_dir = os.path.dirname(input_path_text)
        
        if self.zip_output_checkbox.isChecked() and final_output_dir and os.path.isdir(final_output_dir):
            try:
                zip_filename_base = os.path.basename(os.path.normpath(final_output_dir))
                if not zip_filename_base: # if final_output_dir was something like "C:/", basename is empty
                    zip_filename_base = "converted_images"
                zip_filename = zip_filename_base + ".zip"

                # Place zip in the parent of the final_output_dir
                zip_file_parent_dir = os.path.dirname(final_output_dir)
                if not zip_file_parent_dir: # if final_output_dir is a root drive (e.g. C:/)
                    zip_file_parent_dir = final_output_dir # place it inside itself (less ideal but avoids error)

                zip_filepath = os.path.join(zip_file_parent_dir, zip_filename)

                self.status_output.append(f"Zipping folder: {final_output_dir} to {zip_filepath}")
                self.zip_folder(final_output_dir, zip_filepath)
                self.status_output.append(f"Zipped output to: {zip_filepath}")
                QMessageBox.information(self, "Zipping Complete", f"Output folder zipped to {zip_filepath}")
            except Exception as e:
                self.status_output.append(f"Error zipping output: {e}")
                QMessageBox.critical(self, "Error Zipping", f"Could not zip output folder: {e}")
        else:
            if self.zip_output_checkbox.isChecked():
                self.status_output.append(f"Skipping zipping: Could not determine valid output directory '{final_output_dir}'.")


        self.convert_button.setEnabled(True)

    def conversion_error(self, message):
        self.status_output.append(f"Error: {message}")
        QMessageBox.critical(self, "Error", f"Conversion failed: {message}")
        self.convert_button.setEnabled(True)

    def zip_folder(self, folder_path, zip_path):
        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, _, files in os.walk(folder_path):
                for file in files:
                    file_path = os.path.join(root, file)
                    # Arcname is the path inside the zip file
                    arcname = os.path.relpath(file_path, folder_path)
                    zipf.write(file_path, arcname)


if __name__ == "__main__":
    app = QApplication(sys.argv)

    if qt_material:
        try:
            # You can change the theme here, e.g., 'light_blue.xml', 'dark_red.xml'
            # print(qt_material.list_themes()) # To see available themes
            qt_material.apply_stylesheet(app, theme='dark_blue.xml')
        except Exception as e:
            print(f"Could not apply qt-material theme: {e}")
            print("Ensure 'qt-material' is installed: pip install qt-material")
    else:
        print("Skipping Qt Material theme application (qt-material library not found).")

    window = ImageConverterGUI()
    window.show()
    sys.exit(app.exec())
