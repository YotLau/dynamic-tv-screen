import os
import time
from samsungtvws import SamsungTVWS

def push_image_to_tv(image_path):
    try:
        print(f"Initializing TV connection to {os.getenv('TV_IP')}...")
        tv = SamsungTVWS(host=os.getenv("TV_IP"))
        
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
                file_type="JPEG",
                matte="flexible_polar"
            )
            print(f"Upload response received: {response}")
        
        print("Waiting for upload to complete...")
        time.sleep(5)  # Allow TV processing time
        
        print("Selecting uploaded image...")
        selection_response = art.select_image(response)
        print(f"Selection response: {selection_response}")
        print("Upload and selection completed successfully!")
        return True
        
    except Exception as e:
        raise Exception(f"TV upload failed: {str(e)}") 