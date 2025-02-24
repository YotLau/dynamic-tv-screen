import os
import time
from samsungtvws import SamsungTVWS

def push_image_to_tv(image_path, tv_ip):
    try:
        if not tv_ip:
            raise ValueError("TV IP address is required")

        if not image_path:
            raise ValueError("Image path is required")

        print(f"Initializing TV connection to {tv_ip}...")
        tv = SamsungTVWS(host=tv_ip, port=8002)  # Added explicit port
        
        print("Getting art mode interface...")
        art = tv.art()
        
        print("Reading image file...")
        try:
            with open(image_path, "rb") as image_file:
                image_data = image_file.read()
                print(f"Image size: {len(image_data)} bytes")
                
                if len(image_data) == 0:
                    raise ValueError("Image file is empty")
                
                print(f"Uploading image '{image_path}' to Samsung Frame TV...")
                print("This may take a few moments...")
                response = art.upload(
                    image_data,
                    file_type="JPEG",
                    matte="flexible_polar"
                )
                print(f"Upload response received: {response}")
            
            if not response:
                raise ValueError("No response received from TV after upload")
            
            print("Waiting for upload to complete...")
            time.sleep(5)  # Allow TV processing time
            
            print("Attempting to select uploaded image...")
            try:
                selection_response = art.select_image(response)
                print(f"Selection response: {selection_response}")
                
                if not selection_response:
                    print("Warning: Image selection not confirmed by TV, but upload was successful")
            except Exception as select_error:
                print(f"Warning: Could not select image: {str(select_error)}")
                print("Image was uploaded but selection failed - TV may need manual selection")
            
            print("Upload completed successfully!")
            return True
            
        except FileNotFoundError:
            raise ValueError(f"Image file not found: {image_path}")
        except IOError as e:
            raise ValueError(f"Error reading image file: {str(e)}")
            
    except Exception as e:
        error_message = f"TV upload failed: {str(e)}"
        print(error_message)  # Log the error for debugging
        raise Exception(error_message)