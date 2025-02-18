#!/usr/bin/env python3
import os
import tempfile
import requests
import random
from dotenv import load_dotenv

# Load variables from .env file
load_dotenv()

# Constants
NEGATIVE_PROMPT = "ugly, blurry, low quality, distorted, deformed"

def get_random_prompt():
    """
    Randomly selects one of the configured prompts from environment variables.
    """
    prompts = [
        os.getenv('PROMPT_1'),
        os.getenv('PROMPT_2'),
        os.getenv('PROMPT_3'),
        os.getenv('PROMPT_4'),
        os.getenv('PROMPT_5')
    ]
    # Filter out any None values in case some prompts aren't set
    valid_prompts = [p for p in prompts if p]
    if not valid_prompts:
        raise Exception("No valid prompts found in environment variables")
    
    selected_prompt = random.choice(valid_prompts)
    print(f"Selected prompt: {selected_prompt}")
    return selected_prompt

def generate_image_api():
    """
    Generates an image using the Ideogram API.
    Returns the temporary image path.
    """
    try:
        # Get a random prompt
        selected_prompt = get_random_prompt()
        
        response = requests.post(
            "https://api.ideogram.ai/generate",
            headers={
                "Api-Key": os.getenv('IDEOGRAM_API_KEY'),
                "Content-Type": "application/json"
            },
            json={
                "image_request": {
                    "prompt": selected_prompt,
                    "model": os.getenv('IDEOGRAM_MODEL'),
                    "magic_prompt_option": "AUTO",
                    "negative_prompt": os.getenv('NEGATIVE_PROMPT'),
                    "style_type": os.getenv('IDEOGRAM_STYLE_TYPE'),
                    "aspect_ratio": os.getenv('IDEOGRAM_ASPECT_RATIO')
                }
            },
        )
        
        if response.status_code != 200:
            raise Exception(f"Ideogram API request failed with status code: {response.status_code}, response: {response.text}")
        
        result = response.json()
        print(f"API Response: {result}")
        
        # Check for the correct response structure
        if not result.get("data") or not result["data"]:
            raise Exception("Ideogram API response does not contain data array")
            
        # Get the first image from the data array
        image_data = result["data"][0]
        image_url = image_data.get("url")
        
        if not image_url:
            raise Exception("Ideogram API response does not contain an image URL")
        
        print("Ideogram generated image URL:", image_url)
        
        # Download the image and save it temporarily
        temp_dir = tempfile.gettempdir()
        temp_image_path = os.path.join(temp_dir, "ideogram_generated_image.webp")
        r = requests.get(image_url)
        if r.status_code != 200:
            raise Exception(f"Failed to download image from Ideogram. Status code: {r.status_code}")
        with open(temp_image_path, "wb") as f:
            f.write(r.content)
        print("Ideogram image saved temporarily at:", temp_image_path)
        return temp_image_path
    except Exception as e:
        raise Exception("Ideogram generation failed: " + str(e))