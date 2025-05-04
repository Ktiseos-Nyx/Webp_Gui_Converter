# image_converter.py
import os
from PIL import Image
from tqdm import tqdm  # Import tqdm here

def convert_image_to_webp(input_filepath, output_filepath, quality=80, lossless=False):
    """Converts a single image to WebP format."""
    try:
        img = Image.open(input_filepath)
        img.save(output_filepath, 'webp', quality=quality, lossless=lossless)
        return True  # Indicate success
    except FileNotFoundError:
        print(f"Error: Input file not found: {input_filepath}")
        return False
    except Exception as e:
        print(f"Error converting {input_filepath}: {e}")
        return False

def process_images(input_path, output_dir=None, quality=80, lossless=False,
                   recursive=False, no_overwrite=False, progress_callback=None):
    """Processes images based on input path, handling recursion and overwrite."""

    if os.path.isfile(input_path):
        # Single file conversion
        images_to_convert = [input_path]
        input_dir = os.path.dirname(input_path)
    elif os.path.isdir(input_path):
        input_dir = input_path
        images_to_convert = []
        if recursive:
            for root, _, files in os.walk(input_path):
                for file in files:
                    if file.lower().endswith(('.png', '.jpg', '.jpeg')):
                        images_to_convert.append(os.path.join(root, file))
        else:
            for file in os.listdir(input_path):
                if os.path.isfile(os.path.join(input_path, file)) and file.lower().endswith(('.png', '.jpg', '.jpeg')):
                    images_to_convert.append(os.path.join(input_path, file))
    else:
        print(f"Error: Invalid input path: {input_path}")
        return

    if not images_to_convert:
        print("No PNG or JPG images found.")
        return

    if output_dir is None:
        output_dir = input_dir

    if not os.path.exists(output_dir):
        os.makedirs(output_dir, exist_ok=True)

    total_images = len(images_to_convert)

    with tqdm(total=total_images, desc="Converting Images", disable=(progress_callback is not None)) as pbar:
        for input_filepath in images_to_convert:
            try:
                filename = os.path.basename(input_filepath)
                base_filename, _ = os.path.splitext(filename)
                output_webp_filename = base_filename + ".webp"
                output_webp_filepath = os.path.join(output_dir, output_webp_filename)

                if no_overwrite and os.path.exists(output_webp_filepath):
                    print(f"Skipping {filename} (already exists).")
                    pbar.update(1)
                    continue

                if convert_image_to_webp(input_filepath, output_webp_filepath, quality, lossless):
                    pbar.update(1)
                    if progress_callback:
                        progress_callback(pbar.n, total_images, f"Converted: {filename}") # Send progress to GUI
                else:
                    print(f"Failed to convert {filename}")

            except Exception as e:
                print(f"Error processing {filename}: {e}")

    print("Conversion complete!")
