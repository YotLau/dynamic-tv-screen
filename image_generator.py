#!/usr/bin/env python3
import os
import tempfile
import requests
from prompt_generator import PromptGenerator

# Constants
NEGATIVE_PROMPT = "ugly, blurry, low quality, distorted, deformed"

def get_random_prompt():
    generator = PromptGenerator()
    return generator.generate_prompt() or "A beautiful digital artwork with vibrant colors and dynamic composition"

def generate_image_api():
    try:
        response = requests.post(
            "https://api.ideogram.ai/generate",
            headers={
                "Api-Key": os.getenv('IDEOGRAM_API_KEY'),
                "Content-Type": "application/json"
            },
            json={
                "image_request": {
                    "prompt": get_random_prompt(),
                    "model": os.getenv('IDEOGRAM_MODEL'),
                    "magic_prompt_option": "AUTO",
                    "negative_prompt": os.getenv('NEGATIVE_PROMPT'),
                    "style_type": os.getenv('IDEOGRAM_STYLE_TYPE'),
                    "aspect_ratio": os.getenv('IDEOGRAM_ASPECT_RATIO')
                }
            }
        )
        response.raise_for_status()
        
        result = response.json()
        image_url = result.get("data", [{}])[0].get("url")
        if not image_url:
            return None
            
        print(f"Ideogram generated image URL: {image_url}")
        
        temp_image_path = os.path.join(tempfile.gettempdir(), "ideogram_generated_image.webp")
        with open(temp_image_path, "wb") as f:
            f.write(requests.get(image_url).content)
            
        print(f"Ideogram image saved temporarily at: {temp_image_path}")
        return temp_image_path
        
    except Exception as e:
        raise Exception(f"Ideogram generation failed: {str(e)}")