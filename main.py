#!/usr/bin/env python3
import os
from pathlib import Path
from config import Config
from logger import setup_logger
from image_generator import generate_image_api
from image_fetcher import fetch_image
from tv_pusher import push_image_to_tv

logger = setup_logger()

def main():
    try:
        # Validate environment
        Config.validate_env()
        
        # Generate and process image
        temp_image_path = generate_image_api()
        if not temp_image_path or not os.path.exists(temp_image_path):
            logger.error("Failed to generate image")
            return
            
        logger.info(f"Image generated successfully at: {temp_image_path}")
        logger.info(f"Saving to folder: {Config.get_env('IMAGES_FOLDER')}")
        
        try:
            saved_image_path = fetch_image(temp_image_path, Config.get_env('IMAGES_FOLDER'))
            push_image_to_tv(saved_image_path)
            
            # Cleanup temporary file
            os.remove(temp_image_path)
            logger.info("Temporary file cleaned up")
            
            logger.info("Process completed successfully!")
            
        finally:
            # Ensure temp file cleanup even if TV push fails
            if os.path.exists(temp_image_path):
                os.remove(temp_image_path)
                
    except Exception as e:
        logger.error(f"Error: {str(e)}", exc_info=True)

if __name__ == "__main__":
    main()