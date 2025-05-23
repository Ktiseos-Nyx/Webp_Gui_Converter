# image_converter.py
import os
import sys # For dummy image creation in __main__
from PIL import Image
# tqdm is optional here if progress_callback is always used by the GUI
# but good for standalone use or debugging.
from tqdm import tqdm

def convert_image_to_webp(input_filepath, output_filepath, quality=80, lossless=False):
    """Converts a single image to WebP format."""
    try:
        img = Image.open(input_filepath)
        # Ensure output directory for this specific file exists
        os.makedirs(os.path.dirname(output_filepath), exist_ok=True)
        img.save(output_filepath, 'webp', quality=quality, lossless=lossless)
        return True  # Indicate success
    except FileNotFoundError:
        # This error should ideally be caught before calling this function if input_filepath comes from a list
        print(f"Error: Input file not found during conversion: {input_filepath}")
        return False
    except Exception as e:
        print(f"Error converting {input_filepath} to {output_filepath}: {e}")
        return False

def process_images(input_path, output_dir=None, quality=80, lossless=False,
                   recursive=False, no_overwrite=False, progress_callback=None):
    """
    Processes images (PNG, JPG, JPEG) from input_path and converts them to WebP.

    Args:
        input_path (str): Path to a single image file or a directory of images.
        output_dir (str, optional): Directory to save converted WebP images.
                                    If None, WebP images are saved alongside originals.
                                    If recursive and output_dir is specified, subfolder
                                    structure from input_path is mirrored in output_dir.
        quality (int): WebP quality setting (0-100).
        lossless (bool): If True, use lossless WebP compression.
        recursive (bool): If True and input_path is a directory, process subdirectories.
        no_overwrite (bool): If True, do not overwrite existing WebP files in the output.
        progress_callback (function, optional): Callback for progress updates.
                                                Expected signature: func(current, total, message_str)
    """

    images_to_convert = []
    base_input_dir = "" # Used for structuring recursive output

    if os.path.isfile(input_path):
        if input_path.lower().endswith(('.png', '.jpg', '.jpeg', '.tiff', '.bmp')): # Added more common types
            images_to_convert = [input_path]
            base_input_dir = os.path.dirname(input_path)
        else:
            message = f"Input is not a supported image file: {input_path}"
            if progress_callback:
                progress_callback(0, 0, message)
            else:
                print(message)
            return
    elif os.path.isdir(input_path):
        base_input_dir = input_path
        image_extensions = ('.png', '.jpg', '.jpeg', '.tiff', '.bmp') # Added more common types
        if recursive:
            for root, _, files in os.walk(input_path):
                for file in files:
                    if file.lower().endswith(image_extensions):
                        images_to_convert.append(os.path.join(root, file))
        else:
            for file in os.listdir(input_path):
                filepath = os.path.join(input_path, file)
                if os.path.isfile(filepath) and file.lower().endswith(image_extensions):
                    images_to_convert.append(filepath)
    else:
        message = f"Error: Invalid input path: {input_path}"
        if progress_callback:
            progress_callback(0, 0, message)
        else:
            print(message)
        return

    if not images_to_convert:
        message = "No supported image files (PNG, JPG, JPEG, TIFF, BMP) found to convert."
        if progress_callback:
            progress_callback(0, 0, message)
        else:
            print(message)
        return

    total_images = len(images_to_convert)
    converted_count = 0
    skipped_count = 0
    failed_count = 0

    with tqdm(total=total_images, desc="Converting Images", unit="img", disable=(progress_callback is not None)) as pbar:
        for i, input_filepath in enumerate(images_to_convert):
            current_progress = i + 1 # 1-based index for progress reporting
            filename = os.path.basename(input_filepath)
            base_filename, _ = os.path.splitext(filename)
            output_webp_filename = base_filename + ".webp"
            
            target_output_dir_for_file = ""
            if output_dir:
                if recursive and os.path.isdir(base_input_dir) and base_input_dir != os.path.dirname(input_filepath):
                    relative_subdir = os.path.relpath(os.path.dirname(input_filepath), start=base_input_dir)
                    target_output_dir_for_file = os.path.join(output_dir, relative_subdir)
                else: # Not recursive, or file is in root of base_input_dir, or input was single file
                    target_output_dir_for_file = output_dir
            else:
                target_output_dir_for_file = os.path.dirname(input_filepath)

            if not os.path.exists(target_output_dir_for_file):
                try:
                    os.makedirs(target_output_dir_for_file, exist_ok=True)
                except OSError as e:
                    message = f"Error creating output subdirectory {target_output_dir_for_file} for {filename}: {e}"
                    if progress_callback:
                        progress_callback(current_progress, total_images, message)
                    else:
                        print(message)
                    pbar.update(1)
                    failed_count +=1
                    continue

            output_webp_filepath = os.path.join(target_output_dir_for_file, output_webp_filename)

            if no_overwrite and os.path.exists(output_webp_filepath):
                message = f"Skipping: {filename} (already exists)" # Simpler message for GUI
                if progress_callback:
                    progress_callback(current_progress, total_images, message)
                else:
                    # More detailed for CLI
                    print(f"Skipping: {filename} (already exists at {os.path.relpath(output_webp_filepath, output_dir if output_dir else base_input_dir)})")
                pbar.update(1)
                skipped_count +=1
                continue

            try:
                if convert_image_to_webp(input_filepath, output_webp_filepath, quality, lossless):
                    converted_count += 1
                    message = f"Converted: {filename}" # Simpler message for GUI
                    if progress_callback:
                        progress_callback(current_progress, total_images, message)
                    else:
                        # More detailed for CLI
                        print(f"Converted: {filename} -> {os.path.relpath(output_webp_filepath, output_dir if output_dir else base_input_dir)}")
                else:
                    failed_count += 1
                    message = f"Failed to convert {filename}."
                    if progress_callback:
                        progress_callback(current_progress, total_images, message)
                    # convert_image_to_webp prints its own error, so no extra print here for CLI
            except Exception as e:
                failed_count += 1
                message = f"Unexpected error processing {filename}: {e}"
                if progress_callback:
                    progress_callback(current_progress, total_images, message)
                else:
                    print(message)
            finally:
                 pbar.update(1)

    summary_message = f"Finished. Converted: {converted_count}, Skipped: {skipped_count}, Failed: {failed_count}."
    if progress_callback:
        progress_callback(total_images, total_images, summary_message)
    else:
        print(summary_message)

# Example standalone usage:
if __name__ == '__main__':
    # Create dummy files/folders for testing
    test_input_dir = "test_input_converter"
    test_output_dir = "test_output_converter"

    if not os.path.exists(os.path.join(test_input_dir, "subdir")):
        os.makedirs(os.path.join(test_input_dir, "subdir"), exist_ok=True)
    
    try:
        Image.new('RGB', (60, 30), color = 'red').save(os.path.join(test_input_dir, "img1.png"))
        Image.new('RGB', (60, 30), color = 'blue').save(os.path.join(test_input_dir, "img2.jpg"))
        Image.new('RGB', (60, 30), color = 'green').save(os.path.join(test_input_dir, "subdir", "img3.jpeg"))
    except ImportError:
        print("Pillow not installed, cannot create dummy images for test.")
        sys.exit(1)
    except Exception as e:
        print(f"Error creating dummy images: {e}")
        sys.exit(1)

    if not os.path.exists(test_output_dir):
        os.makedirs(test_output_dir)

    print(f"--- Test 1: Recursive conversion to '{os.path.join(test_output_dir, 'recursive_test')}' ---")
    process_images(test_input_dir, output_dir=os.path.join(test_output_dir, 'recursive_test'), recursive=True)
    
    print(f"\n--- Test 2: Non-recursive to '{os.path.join(test_output_dir, 'non_recursive_test')}' ---")
    process_images(test_input_dir, output_dir=os.path.join(test_output_dir, 'non_recursive_test'), recursive=False)

    print(f"\n--- Test 3: Single file to '{test_output_dir}' ---")
    process_images(os.path.join(test_input_dir, "img1.png"), output_dir=test_output_dir)

    print(f"\n--- Test 4: Recursive, no output_dir (save alongside) ---")
    process_images(test_input_dir, output_dir=None, recursive=True, no_overwrite=True)

    print("\nStandalone tests complete. Check directories and console output.")
