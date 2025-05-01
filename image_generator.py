#!/usr/bin/env python3
import os
import requests
from prompt_generator import PromptGenerator
from logger import setup_logger

# Set up logger
logger = setup_logger()

# Constants
NEGATIVE_PROMPT = "ugly, blurry, low quality, distorted, deformed"

def get_random_prompt():
    generator = PromptGenerator()
    prompt = generator.generate_prompt()
    if not prompt:
        logger.error("Failed to generate prompt")
        return None
    return prompt

def generate_image_api(prompt):
    try:
        # Check if API key is set
        api_key = os.getenv('IDEOGRAM_API_KEY')
        if not api_key:
            logger.error("IDEOGRAM_API_KEY is not set in environment variables")
            raise ValueError("IDEOGRAM_API_KEY is not configured")

        if not prompt:
            return None
            
        logger.info(f"Using prompt: {prompt}")
        
        # Prepare request payload as files
        files_payload = {
            'prompt': (None, prompt),
            'magic_prompt': (None, "AUTO"),
            'negative_prompt': (None, os.getenv('NEGATIVE_PROMPT', NEGATIVE_PROMPT)),
            'style_type': (None, os.getenv('IDEOGRAM_STYLE_TYPE', 'AUTO')),
            'aspect_ratio': (None, os.getenv('IDEOGRAM_ASPECT_RATIO', '16x9'))
        }

        logger.info("Making request to Ideogram API")
        response = requests.post(
            "https://api.ideogram.ai/v1/ideogram-v3/generate",
            headers={
                "Api-Key": api_key
                # Content-Type is automatically set to multipart/form-data by requests when using 'files'
            },
            files=files_payload
        )

        # Log the response status
        logger.info(f"Ideogram API response status: {response.status_code}")
        
        if response.status_code == 404:
            logger.error("Ideogram API endpoint not found (404)")
            raise Exception("Ideogram API endpoint not found. Please check the API URL.")
        
        response.raise_for_status()
        
        result = response.json()
        image_url = result.get("data", [{}])[0].get("url")
        if not image_url:
            logger.error("No image URL in response")
            return None
            
        logger.info(f"Successfully generated image URL: {image_url}")
        return image_url
        
    except requests.exceptions.RequestException as e:
        logger.error(f"Request to Ideogram API failed: {str(e)}")
        raise Exception(f"Failed to connect to Ideogram API: {str(e)}")
    except ValueError as e:
        logger.error(f"Configuration error: {str(e)}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error in image generation: {str(e)}")
        raise Exception(f"Image generation failed: {str(e)}")
