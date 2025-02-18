#!/usr/bin/env python3
import os
import shutil
from datetime import datetime
from dotenv import load_dotenv
import tempfile
import requests

# Load variables from .env file
load_dotenv()

# Constants
NEGATIVE_PROMPT = "ugly, blurry, low quality, distorted, deformed"
MainPrompt = os.getenv('PROMPT')  # Change prompt if desired.

# -------------------------------
# Step 1: Image Generation Functions
# -------------------------------

# Hugging Face Generation via gradio_client
from gradio_client import Client

# Initialize the Hugging Face client (update the Space name if needed)
client = Client(os.getenv('IDEOGRAM_ENDPOINT'))

def generate_image_ideogram():
    """
    Generates an image using the Ideogram API.
    Returns the temporary image path.
    """
    try:
        response = requests.post(
            "https://api.ideogram.ai/generate",
            headers={
                "Api-Key": os.getenv('IDEOGRAM_API_KEY'),
                "Content-Type": "application/json"
            },
            json={
                "image_request": {
                    "prompt": os.getenv('PROMPT'),
                    "model": os.getenv('IDEOGRAM_MODEL'),
                    "magic_prompt_option": "AUTO",
                    "negative_prompt": os.getenv('NEGATIVE_PROMPT'),
                    "style_type": os.getenv('IDEOGRAM_STYLE_TYPE'),
                    "resolution": os.getenv('IDEOGRAM_RESOLUTION'),
                    "aspect_ratio": os.getenv('IDEOGRAM_ASPECT_RATIO')
                }
            },
        )
        
        if response.status_code != 200:
            raise Exception(f"Ideogram API request failed with status code: {response.status_code}, response: {response.text}")
        
        result = response.json()
        image_url = result.get("image_url")  # Adjust this based on actual API response structure
        if not image_url:
            raise Exception("Ideogram API response does not contain an image URL.")
        
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

def generate_image_openai():
    """
    Generates an image using OpenAI's image generation API as a fallback.
    Returns the temporary image path.
    """
    # --- PLACEHOLDER: Insert your OpenAI API token below ---
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")  # Replace with your actual OpenAI API key

    url = "https://api.openai.com/v1/images/generations"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {OPENAI_API_KEY}"
    }
    payload = {
        "model": "dall-e-3",
        "prompt": MainPrompt,  # Same prompt as HF; adjust if desired.
        "n": 1,
        "size": "1792x1024"
    }
    print("Requesting image generation from OpenAI...")
    response = requests.post(url, headers=headers, json=payload)
    if response.status_code != 200:
        raise Exception(f"OpenAI API request failed with status code: {response.status_code}, response: {response.text}")
    
    result = response.json()
    if "data" not in result or len(result["data"]) == 0:
        raise Exception("OpenAI API response does not contain image data.")
    
    image_url = result["data"][0].get("url")
    if not image_url:
        raise Exception("OpenAI API response does not contain an image URL.")
    
    print("OpenAI generated image URL:", image_url)
    
    # Download the image from OpenAI and save it temporarily
    temp_dir = tempfile.gettempdir()
    temp_image_path = os.path.join(temp_dir, "openai_generated_image.webp")
    r = requests.get(image_url)
    if r.status_code != 200:
        raise Exception(f"Failed to download image from OpenAI. Status code: {r.status_code}")
    with open(temp_image_path, "wb") as f:
        f.write(r.content)
    print("OpenAI image saved temporarily at:", temp_image_path)
    return temp_image_path

# -------------------------------
# Step 2: Fetch (Copy) the Generated Image
# -------------------------------
def fetch_image(temp_image_path, save_folder):
    """
    Copies the generated image from its temporary location to the desired folder.
    Returns the destination path.
    """
    if not os.path.exists(temp_image_path):
        raise Exception(f"Temporary file not found: {temp_image_path}")

    if not os.path.exists(save_folder):
        os.makedirs(save_folder)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"generated_image_{timestamp}.webp"
    destination_path = os.path.join(save_folder, filename)

    shutil.copy(temp_image_path, destination_path)
    print("Image saved locally at:", destination_path)
    return destination_path

# -------------------------------
# Step 3: Push the Image to the Samsung Frame TV
# -------------------------------
from samsungtvws import SamsungTVWS

# Replace with your TV's local IP address.
TV_IP = os.getenv("TV_IP")  # Update with your actual TV IP

def push_image_to_tv(image_path):
    """
    Reads the saved image file and pushes it to the Samsung Frame TV.
    """
    try:
        tv = SamsungTVWS(host=TV_IP)
        art = tv.art()
        with open(image_path, "rb") as image_file:
            image_data = image_file.read()
        print(f"Uploading image '{image_path}' to Samsung Frame TV...")
        response = art.upload(
            image_data,
            file_type="JPEG",          # Ensure this matches your image format.
            matte="modern_polar"    # Adjust matte style if desired.
        )
        print("Upload successful!")
        print("TV Response:", response)
        tv.art().select_image(response)
    except Exception as e:
        print("Error during upload:", e)

# -------------------------------
# Main Execution Flow
# -------------------------------
def main():
    try:
        # Generate image using Ideogram API
        temp_image_path = generate_image_ideogram()
        
        # Define the folder where images should be stored.
        save_folder = os.getenv('IMAGES_FOLDER')  # Fixed typo from os.env to os.getenv
        
        # Copy the generated image to your designated folder.
        saved_image_path = fetch_image(temp_image_path, save_folder)
        
        # Upload the saved image to your Samsung Frame TV.
        push_image_to_tv(saved_image_path)
        
        print("Process completed successfully!")
    except Exception as e:
        print("Error in process:", e)

if __name__ == "__main__":
    main()
