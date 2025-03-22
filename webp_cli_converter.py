import os
from PIL import Image

def convert_images_to_webp(input_folder, output_folder=None, quality=80, lossless=False):
    """
    Converts PNG and JPG images in the input folder to WebP format and saves them
    in the output folder (or the input folder if output_folder is None).

    Args:
        input_folder (str): Path to the folder containing PNG and JPG images.
        output_folder (str, optional): Path to the folder where WebP images will be saved.
                                       If None, WebP images are saved in the input folder,
                                       replacing the original files (be careful!).
        quality (int, optional): Quality level for lossy WebP compression (0-100). Defaults to 80.
        lossless (bool, optional): Whether to use lossless WebP compression. Defaults to False (lossy).
    """

    if output_folder is None:
        output_folder = input_folder  # Save in the same folder by default

    if not os.path.exists(output_folder):
        os.makedirs(output_folder, exist_ok=True)  # Create output folder if it doesn't exist

    for filename in os.listdir(input_folder):
        if os.path.isfile(os.path.join(input_folder, filename)):
            if filename.lower().endswith(('.png', '.jpg', '.jpeg')):  # Include .jpeg for broader compatibility
                input_filepath = os.path.join(input_folder, filename)
                try:
                    img = Image.open(input_filepath)
                    base_filename, ext = os.path.splitext(filename)
                    output_webp_filename = base_filename + ".webp"
                    output_webp_filepath = os.path.join(output_folder, output_webp_filename)

                    print(f"Converting: {filename} to {output_webp_filename}")

                    img.save(output_webp_filepath, 'webp', quality=quality, lossless=lossless)

                    print(f"Saved: {output_webp_filename}")

                except Exception as e:
                    print(f"Error processing {filename}: {e}")

    print("Conversion complete!")


if __name__ == "__main__":
    input_directory = input("Enter the path to the input folder containing images: ")
    output_directory = input("Enter the path to the output folder (leave blank to save in input folder): ") or None # Allow blank for same folder
    quality_level = int(input("Enter WebP quality (0-100, default 80): ") or 80) # Allow default if blank
    use_lossless = input("Use lossless WebP compression? (yes/no, default no): ").lower() == 'yes' # Allow default

    convert_images_to_webp(input_directory, output_directory, quality=quality_level, lossless=use_lossless)