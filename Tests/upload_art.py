#!/usr/bin/env python3
import sys
from samsungtvws import SamsungTVWS

# Replace with your TV's local IP address.
TV_IP = "192.168.1.225"  # Update with your actual TV IP

def upload_image(image_path):
    try:
        # Establish connection to the TV
        tv = SamsungTVWS(host=TV_IP)
        art = tv.art()

        # Open the image file in binary mode
        with open(image_path, "rb") as image_file:
            image_data = image_file.read()

        print(f"Uploading image '{image_path}' to art mode...")
        # Upload the image using the supported keyword arguments
        response = art.upload(
            image_data,
            file_type="JPEG",         # Specify file type
            matte="flexible_polar"    # Example matte style; change as desired
        )
        print("Upload successful!")
        print("Response:", response)
    except Exception as e:
        print("Error during upload:", e)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: py upload_art.py <path_to_image>")
    else:
        upload_image(sys.argv[1])
