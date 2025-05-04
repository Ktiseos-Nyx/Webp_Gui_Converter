import os
from PIL import Image

def convert_images_to_webp(input_folder, output_folder=None, quality=80, lossless=False):
    """
    Converts PNG and JPG images in the input folder to WebP format and saves them
    in the output folder (or the input folder if output_folder is None).

    Args:
        input_folder (str): Path to the folder containing PNG and JPG images.
        output_folder (str, optional): Path to the folder where WebP images will be saved.
                                       If None, WebP images are saved in the input folder.
        quality (int, optional): Quality level for lossy WebP compression (0-100). Defaults to 80.
        lossless (bool, optional): Whether to use lossless WebP compression. Defaults to False (lossy).
    """

    if not os.path.isdir(input_folder):
        print(f"Error: Input folder '{input_folder}' does not exist or is not a directory.")
        return

    if output_folder is None:
        output_folder = input_folder  # Save in the same folder by default

    if not os.path.exists(output_folder):
        os.makedirs(output_folder, exist_ok=True)  # Create output folder if it doesn't exist

    if not 0 <= quality <= 100:
        print("Error: Quality must be between 0 and 100.  Using default quality of 80.")
        quality = 80

    image_files_found = False
    valid_extensions = {'.png', '.jpg', '.jpeg'} # Use a set for faster lookups

    for filename in os.listdir(input_folder):
        if os.path.isfile(os.path.join(input_folder, filename)):
            if os.path.splitext(filename.lower())[1] in valid_extensions:
                image_files_found = True
                input_filepath = os.path.join(input_folder, filename)
                try:
                    img = Image.open(input_filepath)
                    base_filename, ext = os.path.splitext(filename)
                    output_webp_filename = base_filename + ".webp"
                    output_webp_filepath = os.path.join(output_folder, output_webp_filename)

                    print(f"Converting: {filename} to {output_webp_filename}\n")

                    img.save(output_webp_filepath, 'webp', quality=quality, lossless=lossless)

                    print(f"Saved: {output_webp_filename}\n")

                except Exception as e:
                    print(f"Error processing {filename}: {e}")

    if not image_files_found:
        print("No PNG or JPG images found in the input folder.")
    else:
        print("Conversion complete!")


if __name__ == "__main__":
    input_directory = input("Enter the path to the input folder containing images: ")
    output_directory = input("Enter the path to the output folder (leave blank to save in input folder): ") or None # Allow blank for same folder

    while True:
        quality_input = input("Enter WebP quality (0-100, default 80): ") or "80" # Allow default if blank
        try:
            quality_level = int(quality_input)
            break  # Exit loop if conversion to int is successful
        except ValueError:
            print("Invalid input. Please enter an integer between 0 and 100.")

    lossless_input = input("Use lossless WebP compression? (yes/no, default no): ").lower()
    use_lossless = lossless_input in ('yes', 'y', 'true') # Allow 'y' and 'true'

    convert_images_to_webp(input_directory, output_directory, quality=quality_level, lossless=use_lossless)
