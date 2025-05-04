# cli_script.py
import argparse
import image_converter  # Import the shared module

def main():
    parser = argparse.ArgumentParser(description="Convert images to WebP format.")
    parser.add_argument("input_path", help="Path to the input folder or file.")
    parser.add_argument("-o", "--output_dir", help="Path to the output directory (optional).")
    parser.add_argument("-q", "--quality", type=int, default=80, help="WebP quality (0-100).")
    parser.add_argument("-l", "--lossless", action="store_true", help="Use lossless compression.")
    parser.add_argument("-r", "--recursive", action="store_true", help="Process subfolders recursively.")
    parser.add_argument("-n", "--no_overwrite", action="store_true", help="Prevent overwriting existing files.")

    args = parser.parse_args()

    if not 0 <= args.quality <= 100:
        print("Error: Quality must be between 0 and 100.")
        return

    image_converter.process_images(args.input_path, args.output_dir, args.quality, args.lossless,
                                  args.recursive, args.no_overwrite)


if __name__ == "__main__":
    main()
