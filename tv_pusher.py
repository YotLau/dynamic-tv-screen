import os
import time
from dotenv import load_dotenv
from samsungtvws import SamsungTVWS

# Load variables from .env file
load_dotenv()

# TV Configuration
TV_IP = os.getenv("TV_IP")

def push_image_to_tv(image_path):
    """
    Reads the saved image file and pushes it to the Samsung Frame TV.
    """
    try:
        print(f"Initializing TV connection to {TV_IP}...")
        tv = SamsungTVWS(host=TV_IP)
        
        print("Getting art mode interface...")
        art = tv.art()
        
        print("Reading image file...")
        with open(image_path, "rb") as image_file:
            image_data = image_file.read()
            print(f"Image size: {len(image_data)} bytes")
        
        print(f"Uploading image '{image_path}' to Samsung Frame TV...")
        print("This may take a few moments...")
        
        response = art.upload(
            image_data,
            file_type="JPEG",          # Ensure this matches your image format.
            matte="flexible_polar"  
        )
        print("Upload response received:", response)
        
        print("Waiting for upload to complete...")
        time.sleep(5)  # Give the TV some time to process
        
        print("Selecting uploaded image...")
        selection_response = art.select_image(response)
        print("Selection response:", selection_response)
        
        print("Upload and selection completed successfully!")
        return True
        
    except Exception as e:
        print(f"Detailed error in TV upload: {str(e)}")
        print(f"Error type: {type(e).__name__}")
        if hasattr(e, 'response'):
            print(f"Response status code: {e.response.status_code}")
            print(f"Response content: {e.response.content}")
        raise Exception(f"TV upload failed: {str(e)}") 