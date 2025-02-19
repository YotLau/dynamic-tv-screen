#!/usr/bin/env python3
import os
import argparse
from dotenv import load_dotenv
from image_generator import generate_image_api
from image_fetcher import fetch_image
from combine_logo_background import combine_images

# Load variables from .env file
load_dotenv()

def main():
    # Set up argument parser
    parser = argparse.ArgumentParser(description='Generate background and combine with logo')
    parser.add_argument('logo_path', type=str, help='Path to the logo file')
    args = parser.parse_args()

    try:
        # Generate image using Ideogram API
        temp_image_path = generate_image_api()
        
        # Define the folder where images should be stored
        save_folder = os.getenv('IMAGES_FOLDER')
        
        # Copy the generated image to designated folder
        saved_image_path = fetch_image(temp_image_path, save_folder)
        
        # Create output path for the combined image
        output_filename = f"combined_{os.path.basename(saved_image_path)}"
        output_path = os.path.join(save_folder, output_filename)
        
        # Combine the logo with the background (logo on top)
        final_image = combine_images(args.logo_path, saved_image_path, output_path)
        
        print(f"Process completed successfully! Final image saved at: {final_image}")
    except Exception as e:
        print("Error in process:", e)

if __name__ == "__main__":
    main() 