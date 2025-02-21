#!/usr/bin/env python3
import os
from pathlib import Path
from dotenv import load_dotenv
from image_generator import generate_image_api
from image_fetcher import fetch_image
from tv_pusher import push_image_to_tv

def main():
    try:
        # Verify required environment variables
        required_vars = ['OPENROUTER_API_KEY', 'OPENROUTER_MODEL', 'IMAGES_FOLDER']
        missing_vars = [var for var in required_vars if not os.getenv(var)]
        if missing_vars:
            raise ValueError(f"Missing required environment variables: {', '.join(missing_vars)}")
            
        # Generate and process image
        temp_image_path = generate_image_api()
        if not temp_image_path or not os.path.exists(temp_image_path):
            return
            
        print(f"Image generated successfully at: {temp_image_path}")
        print(f"Saving to folder: {os.getenv('IMAGES_FOLDER')}")
        
        saved_image_path = fetch_image(temp_image_path, os.getenv('IMAGES_FOLDER'))
        push_image_to_tv(saved_image_path)
        
        print("Process completed successfully!")
        
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    main() 