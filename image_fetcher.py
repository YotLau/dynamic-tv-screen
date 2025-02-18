import os
import shutil
from datetime import datetime

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