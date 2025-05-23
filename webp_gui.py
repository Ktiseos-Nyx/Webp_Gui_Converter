import sys
import os
import zipfile
from functools import partial

from PyQt6.QtWidgets import (QApplication, QMainWindow, QLabel, QLineEdit,
                             QPushButton, QVBoxLayout, QHBoxLayout, QWidget,
                             QFileDialog, QSpinBox, QCheckBox, QTextEdit,
                             QMessageBox, QProgressBar, QDialog,
                             QDialogButtonBox)
from PyQt6.QtGui import QAction, QIcon # Added QIcon
from PyQt6.QtCore import Qt, QThread, pyqtSignal, QSize # Added QSize

try:
    import qt_material
except ImportError:
    print("qt-material library not found. Consider installing it: pip install qt-material")
    qt_material = None

# This will import the image_converter.py file you save in the same directory
import image_converter

class NewFolderDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Create New Folder")
        # self.setWindowIcon(QIcon("path/to/your/icon.png")) # Optional: Set icon for dialog

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
        # Apply qt-material style to dialog if available
        if qt_material and hasattr(self.parent(), 'current_theme_name'):
             qt_material.apply_stylesheet(self, theme=self.parent().current_theme_name)


    def getFolderName(self):
        return self.lineEdit.text()

class ConversionThread(QThread):
    progress_update = pyqtSignal(int, int, str)
    finished_signal = pyqtSignal(str)
    error_signal = pyqtSignal(str)

    def __init__(self, input_path, output_dir, quality, lossless, recursive, no_overwrite, zip_output):
        super().__init__()
        self.input_path = input_path
        self.output_dir = output_dir
        self.quality = quality
        self.lossless = lossless
        self.recursive = recursive
        self.no_overwrite = no_overwrite
        self.zip_output = zip_output # Retained, though zipping logic is in GUI

    def run(self):
        try:
            image_converter.process_images(
                self.input_path, self.output_dir, self.quality, self.lossless,
                self.recursive, self.no_overwrite, self.progress_update.emit
            )
            # The finished signal now passes the effective output directory used by process_images
            # For simplicity, we'll pass the originally intended output_dir.
            # The zipping logic in GUI will re-determine the actual output if output_dir was None.
            self.finished_signal.emit(self.output_dir if self.output_dir else self.input_path)
        except Exception as e:
            self.error_signal.emit(f"Error in conversion thread: {str(e)}")


class ImageConverterGUI(QMainWindow):
    PREDEFINED_SIZES = {
        "Default (600x650)": (600, 650),
        "Portrait - Small (500x700)": (500, 700),
        "Portrait - Tall (600x800)": (600, 800),
        "Square - Small (700x700)": (700, 700),
        "Landscape - Small (800x600)": (800, 600),
        "Landscape - Medium (1024x768)": (1024, 768),
    }
    DEFAULT_SIZE_NAME = "Default (600x650)"
    DEFAULT_THEME = 'dark_blue.xml' # Default qt-material theme

    def __init__(self):
        super().__init__()
        self.current_theme_name = self.DEFAULT_THEME # Store current theme
        self.setWindowTitle("Image to WebP Converter")
        # self.setWindowIcon(QIcon("path/to/your/main/icon.ico")) # Optional: Set main window icon

        initial_width, initial_height = self.PREDEFINED_SIZES[self.DEFAULT_SIZE_NAME]
        self.setFixedSize(initial_width, initial_height)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)

        self._create_menu_bar()
        self._create_ui_elements()

        self.toggle_output_folder_widgets(self.output_folder_checkbox.checkState().value)


    def _create_ui_elements(self):
        # Input Folder
        input_folder_layout = QHBoxLayout()
        self.input_folder_label = QLabel("Input Folder/File:")
        self.input_folder_line_edit = QLineEdit()
        self.input_folder_line_edit.setPlaceholderText("Path to image or folder of images")
        self.browse_input_button = QPushButton("Browse...")
        self.browse_input_button.setIcon(QIcon.fromTheme("document-open", QIcon(":/qt-project.org/styles/commonstyle/images/standardbutton-open-16.png"))) # Example icon
        self.browse_input_button.clicked.connect(self.browse_input)
        input_folder_layout.addWidget(self.input_folder_label)
        input_folder_layout.addWidget(self.input_folder_line_edit)
        input_folder_layout.addWidget(self.browse_input_button)
        self.layout.addLayout(input_folder_layout)

        # Output Folder Checkbox
        self.output_folder_checkbox = QCheckBox("Use Separate Output Folder")
        self.output_folder_checkbox.stateChanged.connect(self.toggle_output_folder_widgets)
        self.layout.addWidget(self.output_folder_checkbox)

        # Output Folder Path
        self.output_folder_layout = QHBoxLayout()
        self.output_folder_label = QLabel("Output Folder:")
        self.output_folder_line_edit = QLineEdit()
        self.output_folder_line_edit.setPlaceholderText("Leave blank to save alongside input")
        self.browse_output_button = QPushButton("Browse...")
        self.browse_output_button.setIcon(QIcon.fromTheme("folder-open", QIcon(":/qt-project.org/styles/commonstyle/images/standardbutton-open-16.png"))) # Example icon
        self.browse_output_button.clicked.connect(self.browse_output_folder)
        self.output_folder_layout.addWidget(self.output_folder_label)
        self.output_folder_layout.addWidget(self.output_folder_line_edit)
        self.output_folder_layout.addWidget(self.browse_output_button)
        self.layout.addLayout(self.output_folder_layout)

        # Create Output Folder Button
        self.create_output_folder_button = QPushButton("Create New Output Subfolder...")
        self.create_output_folder_button.setIcon(QIcon.fromTheme("folder-new", QIcon(":/qt-project.org/styles/commonstyle/images/standardbutton-new-16.png"))) # Example icon
        self.create_output_folder_button.clicked.connect(self.create_output_folder)
        self.layout.addWidget(self.create_output_folder_button)

        self.output_folder_hint_label = QLabel() # Text set in toggle_output_folder_widgets
        self.output_folder_hint_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.output_folder_hint_label)

        # WebP Settings
        webp_settings_layout = QHBoxLayout()
        self.quality_label = QLabel("WebP Quality (0-100):")
        self.quality_spinbox = QSpinBox()
        self.quality_spinbox.setRange(0, 100)
        self.quality_spinbox.setValue(80)
        self.quality_spinbox.setToolTip("Higher is better quality, larger file. 0 for smallest (lowest quality).")
        webp_settings_layout.addWidget(self.quality_label)
        webp_settings_layout.addWidget(self.quality_spinbox)
        self.layout.addLayout(webp_settings_layout)

        self.lossless_checkbox = QCheckBox("Lossless Compression")
        self.lossless_checkbox.setToolTip("Results in larger files but no quality loss. Overrides quality setting.")
        self.layout.addWidget(self.lossless_checkbox)

        # Options
        options_layout = QHBoxLayout()
        self.recursive_checkbox = QCheckBox("Process Subfolders")
        self.recursive_checkbox.setToolTip("If input is a folder, also convert images in its subfolders.")
        options_layout.addWidget(self.recursive_checkbox)

        self.overwrite_checkbox = QCheckBox("Overwrite Existing WebP")
        self.overwrite_checkbox.setChecked(False) # Default to NOT overwrite
        self.overwrite_checkbox.setToolTip("If unchecked, existing .webp files with the same name will be skipped.")
        options_layout.addWidget(self.overwrite_checkbox)
        self.layout.addLayout(options_layout)

        self.zip_output_checkbox = QCheckBox("Zip Output After Conversion")
        self.zip_output_checkbox.setToolTip("If a separate output folder is used, zip its contents after conversion.")
        self.layout.addWidget(self.zip_output_checkbox)

        self.progress_bar = QProgressBar()
        self.progress_bar.setTextVisible(True)
        self.layout.addWidget(self.progress_bar)

        self.convert_button = QPushButton("Convert to WebP")
        self.convert_button.setIcon(QIcon.fromTheme("document-save", QIcon(":/qt-project.org/styles/commonstyle/images/standardbutton-save-16.png"))) # Example icon
        self.convert_button.clicked.connect(self.start_conversion)
        self.layout.addWidget(self.convert_button)

        self.status_output = QTextEdit()
        self.status_output.setReadOnly(True)
        self.status_output.setPlaceholderText("Conversion status will appear here...")
        self.layout.addWidget(self.status_output)

    def _create_menu_bar(self):
        menu_bar = self.menuBar()
        
        # File Menu
        file_menu = menu_bar.addMenu("&File")
        exit_action = QAction(QIcon.fromTheme("application-exit"), "&Exit", self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

        # View Menu
        view_menu = menu_bar.addMenu("&View")
        size_menu = view_menu.addMenu("Set Window &Size")
        for name, (width, height) in self.PREDEFINED_SIZES.items():
            action = QAction(name, self)
            action.triggered.connect(partial(self._set_selected_window_size, width, height))
            size_menu.addAction(action)
        
        if qt_material:
            view_menu.addSeparator()
            theme_menu = view_menu.addMenu("&Theme")
            # Get a sorted list of themes
            available_themes = sorted(qt_material.list_themes())
            for theme_file in available_themes:
                theme_name = theme_file.replace('.xml', '').replace('_', ' ').title()
                action = QAction(theme_name, self, checkable=True)
                action.setProperty("theme_file", theme_file) # Store theme filename
                if theme_file == self.current_theme_name:
                    action.setChecked(True)
                action.triggered.connect(self._change_theme)
                theme_menu.addAction(action)
            self.theme_menu = theme_menu # Store reference for updating checks


    def _set_selected_window_size(self, width, height):
        self.setFixedSize(width, height)

    def _change_theme(self):
        action = self.sender()
        if action and action.isChecked():
            new_theme_file = action.property("theme_file")
            try:
                qt_material.apply_stylesheet(QApplication.instance(), theme=new_theme_file)
                self.current_theme_name = new_theme_file # Update current theme
                # Update check marks in theme menu
                for act in self.theme_menu.actions():
                    act.setChecked(act.property("theme_file") == new_theme_file)
            except Exception as e:
                QMessageBox.warning(self, "Theme Error", f"Could not apply theme '{new_theme_file}': {e}")
                action.setChecked(False) # Revert check if failed

    def browse_input(self):
        current_path_in_lineedit = self.input_folder_line_edit.text().strip()
        start_dir = os.path.dirname(current_path_in_lineedit) if current_path_in_lineedit and (os.path.isfile(current_path_in_lineedit) or os.path.isdir(current_path_in_lineedit)) else os.path.expanduser("~")
        if not os.path.isdir(start_dir): # Ensure start_dir is a valid directory
             start_dir = os.path.expanduser("~")

        # --- Option 1: Prioritize Folder Selection (fixes "can't select folder") ---
        # This will first open a dialog to select a folder.
        # If the user cancels, it then opens a dialog to select a single file.
        
        # Ask user what they want to select
        msg_box = QMessageBox(self)
        msg_box.setWindowTitle("Select Input Type")
        msg_box.setText("What do you want to select as input?")
        folder_button = msg_box.addButton("Select Folder", QMessageBox.ButtonRole.ActionRole)
        file_button = msg_box.addButton("Select File", QMessageBox.ButtonRole.ActionRole)
        cancel_button = msg_box.addButton(QMessageBox.StandardButton.Cancel)
        # Apply theme to this QMessageBox if possible
        if qt_material and hasattr(self, 'current_theme_name'):
             qt_material.apply_stylesheet(msg_box, theme=self.current_theme_name)
        
        msg_box.exec()

        selected_path = ""

        if msg_box.clickedButton() == folder_button:
            path = QFileDialog.getExistingDirectory(
                self,
                "Select Input Folder",
                start_dir
            )
            if path:
                selected_path = path
        elif msg_box.clickedButton() == file_button:
            path, _ = QFileDialog.getOpenFileName(
                self,
                "Select Input File",
                start_dir,
                "Image Files (*.png *.jpg *.jpeg *.bmp *.tiff);;All Files (*)"
            )
            if path:
                selected_path = path
        # If cancel_button or dialog closed, selected_path remains empty

        if selected_path:
            self.input_folder_line_edit.setText(selected_path)


    def browse_output_folder(self):
        folder_path = QFileDialog.getExistingDirectory(self, "Select Output Folder")
        if folder_path:
            self.output_folder_line_edit.setText(folder_path)

    def create_output_folder(self):
        parent_for_new_folder = self.output_folder_line_edit.text()
        if not parent_for_new_folder or not os.path.isdir(parent_for_new_folder):
            parent_for_new_folder = self.input_folder_line_edit.text()
            if os.path.isfile(parent_for_new_folder): # If input is file, use its dir
                parent_for_new_folder = os.path.dirname(parent_for_new_folder)

        if not parent_for_new_folder or not os.path.isdir(parent_for_new_folder):
            QMessageBox.warning(self, "Base Folder Missing",
                                "Please select an input or output folder first to create a subfolder in.")
            return

        dialog = NewFolderDialog(self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            folder_name = dialog.getFolderName()
            if not folder_name:
                QMessageBox.warning(self, "Folder Name Missing", "Please enter a subfolder name.")
                return
            
            new_folder_path = os.path.join(parent_for_new_folder, folder_name)
            try:
                os.makedirs(new_folder_path, exist_ok=True)
                self.output_folder_line_edit.setText(new_folder_path)
                if not self.output_folder_checkbox.isChecked():
                    self.output_folder_checkbox.setChecked(True)
            except OSError as e:
                QMessageBox.critical(self, "Error Creating Folder", f"Could not create folder '{new_folder_path}': {e}")

    def toggle_output_folder_widgets(self, state_value):
        enabled = (state_value == Qt.CheckState.Checked.value)
        self.output_folder_label.setEnabled(enabled)
        self.output_folder_line_edit.setEnabled(enabled)
        self.browse_output_button.setEnabled(enabled)
        # Create button is for subfolder, so its enabled state might be different.
        # Let's keep it enabled if either input or output folder is specified.
        # self.create_output_folder_button.setEnabled(enabled)
        self.zip_output_checkbox.setEnabled(enabled) # Zip only makes sense with separate output

        if enabled:
            self.output_folder_hint_label.setText("(WebP files will be saved in the specified output folder)")
        else:
            self.output_folder_hint_label.setText("(WebP files will be saved alongside their originals)")


    def start_conversion(self):
        input_path = self.input_folder_line_edit.text().strip()
        
        output_dir_text = self.output_folder_line_edit.text().strip()
        use_separate_output = self.output_folder_checkbox.isChecked()
        
        output_dir_to_use = output_dir_text if use_separate_output else None

        quality = self.quality_spinbox.value()
        lossless = self.lossless_checkbox.isChecked()
        recursive = self.recursive_checkbox.isChecked()
        no_overwrite = not self.overwrite_checkbox.isChecked()
        zip_output_flag = self.zip_output_checkbox.isChecked() and use_separate_output


        if not input_path:
            QMessageBox.warning(self, "Input Missing", "Please select an input image or folder.")
            return
        if not os.path.exists(input_path):
            QMessageBox.warning(self, "Input Invalid", f"The input path does not exist: {input_path}")
            return
        
        if use_separate_output and not output_dir_to_use:
            QMessageBox.warning(self, "Output Missing", "Please specify an output folder or uncheck 'Use Separate Output Folder'.")
            return
        
        if output_dir_to_use and not os.path.isdir(output_dir_to_use):
            reply = QMessageBox.question(self, "Create Output Folder?",
                                         f"The output folder '{output_dir_to_use}' does not exist. Create it?",
                                         QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
            if reply == QMessageBox.StandardButton.Yes:
                try:
                    os.makedirs(output_dir_to_use, exist_ok=True)
                except OSError as e:
                    QMessageBox.critical(self, "Output Directory Error", f"Could not create output folder: {e}")
                    return
            else:
                return

        self.convert_button.setEnabled(False)
        self.progress_bar.setValue(0)
        self.progress_bar.setFormat("Starting...")
        self.status_output.clear()
        self.status_output.append("Starting conversion...")

        self.conversion_thread = ConversionThread(
            input_path, output_dir_to_use, quality, lossless, 
            recursive, no_overwrite, zip_output_flag # Pass zip_output for thread context if needed later
        )
        self.conversion_thread.progress_update.connect(self.update_progress)
        self.conversion_thread.finished_signal.connect(self.conversion_complete)
        self.conversion_thread.error_signal.connect(self.conversion_error)
        self.conversion_thread.start()

    def update_progress(self, current, total, message):
        if total > 0:
            percentage = int((current / total) * 100)
            self.progress_bar.setValue(percentage)
            self.progress_bar.setFormat(f"{percentage}% ({current}/{total}) - {message}")
        else: # E.g. initial message or if total is 0
            self.progress_bar.setValue(0) # Or set to indeterminate
            self.progress_bar.setFormat(message)
        self.status_output.append(message)
        QApplication.processEvents()

    def conversion_complete(self, thread_output_dir_info):
        # thread_output_dir_info is the output_dir passed to the thread (or input_path if output_dir was None)
        self.status_output.append("------------------------------")
        # The final message from process_images will be in status_output.
        # We can add another one here if needed.
        # self.status_output.append("Conversion process complete from GUI.")
        self.progress_bar.setFormat("Completed!")

        actual_output_location_for_zipping = None
        if self.output_folder_checkbox.isChecked() and self.output_folder_line_edit.text().strip():
            actual_output_location_for_zipping = self.output_folder_line_edit.text().strip()
        
        if self.zip_output_checkbox.isChecked() and actual_output_location_for_zipping:
            if os.path.isdir(actual_output_location_for_zipping):
                self.status_output.append(f"Attempting to zip: {actual_output_location_for_zipping}")
                self.zip_output_folder(actual_output_location_for_zipping)
            else:
                self.status_output.append(f"Skipping zip: Output path '{actual_output_location_for_zipping}' is not a valid directory.")
        
        self.convert_button.setEnabled(True)
        QMessageBox.information(self, "Conversion Finished", "Image conversion process has finished. Check status log for details.")

    def conversion_error(self, message):
        self.status_output.append(f"ERROR: {message}")
        self.progress_bar.setFormat("Error!")
        QMessageBox.critical(self, "Conversion Error", f"An error occurred: {message}")
        self.convert_button.setEnabled(True)

    def zip_output_folder(self, folder_to_zip):
        try:
            # Create zip file in the parent directory of the folder_to_zip
            parent_dir = os.path.dirname(folder_to_zip)
            zip_filename_base = os.path.basename(folder_to_zip)
            if not zip_filename_base: zip_filename_base = "converted_output" # Handle case like "C:/"
            
            zip_filepath = os.path.join(parent_dir if parent_dir else folder_to_zip, f"{zip_filename_base}.zip")

            self.status_output.append(f"Zipping contents of '{folder_to_zip}' to '{zip_filepath}'...")
            with zipfile.ZipFile(zip_filepath, 'w', zipfile.ZIP_DEFLATED) as zipf:
                for root, _, files in os.walk(folder_to_zip):
                    for file in files:
                        file_path = os.path.join(root, file)
                        # arcname is the path inside the zip file, relative to folder_to_zip
                        arcname = os.path.relpath(file_path, folder_to_zip)
                        zipf.write(file_path, arcname)
            self.status_output.append(f"Successfully zipped to: {zip_filepath}")
            QMessageBox.information(self, "Zipping Complete", f"Output successfully zipped to:\n{zip_filepath}")
        except Exception as e:
            self.status_output.append(f"Error during zipping: {e}")
            QMessageBox.critical(self, "Zipping Error", f"Could not zip output folder '{folder_to_zip}':\n{e}")


if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Apply initial theme if qt_material is available
    if qt_material:
        try:
            qt_material.apply_stylesheet(app, theme=ImageConverterGUI.DEFAULT_THEME, invert_secondary=True)
        except Exception as e:
            print(f"Could not apply initial qt-material theme '{ImageConverterGUI.DEFAULT_THEME}': {e}")
    else:
        print("Qt Material library not found. GUI will use default system style.")

    window = ImageConverterGUI()
    window.show()
    sys.exit(app.exec())
