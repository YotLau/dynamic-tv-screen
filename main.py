#!/usr/bin/env python3
import os
from dotenv import load_dotenv
from image_generator import generate_image_api
from image_fetcher import fetch_image
from tv_pusher import push_image_to_tv

# Load variables from .env file
load_dotenv()

def main():
    try:
        # Generate image using Ideogram API
        temp_image_path = generate_image_api()
        
        # Define the folder where images should be stored
        save_folder = os.getenv('IMAGES_FOLDER')
        
        # Copy the generated image to designated folder
        saved_image_path = fetch_image(temp_image_path, save_folder)
        
        # Upload the saved image to Samsung Frame TV
        push_image_to_tv(saved_image_path)
        
        print("Process completed successfully!")
    except Exception as e:
        print("Error in process:", e)

if __name__ == "__main__":
    main() 