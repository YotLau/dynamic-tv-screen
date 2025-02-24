import os
import requests
from datetime import datetime

def fetch_image(image_url, save_folder):
    """
    Downloads an image from a URL and saves it to the specified folder.
    Returns the destination path.
    """
    if not os.path.exists(save_folder):
        os.makedirs(save_folder)

    try:
        response = requests.get(image_url, stream=True)
        response.raise_for_status()

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"generated_image_{timestamp}.jpg"
        destination_path = os.path.join(save_folder, filename)

        with open(destination_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)

        print("Image downloaded and saved locally at:", destination_path)
        return destination_path

    except requests.exceptions.RequestException as e:
        raise Exception(f"Failed to download image from URL: {str(e)}")