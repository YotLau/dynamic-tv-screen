from gradio_client import Client
import shutil
import os
from datetime import datetime

# Initialize the Hugging Face client for the Space
client = Client("black-forest-labs/FLUX.1-schnell")

# Call the API to generate an image.
# Adjust the parameters as needed.
result = client.predict(
    prompt="a beautiful sunset, hyper realism",    # Change prompt if desired.
    seed=0,
    randomize_seed=True,
    width=2048,
    height=1152,
    num_inference_steps=4,
    api_name="/infer"
)
print("API Response:", result)

# The API returns a tuple; the first element is the path to the generated image.
temp_image_path = result[0]
print("Temporary image path:", temp_image_path)

# Ensure the temporary file exists
if not os.path.exists(temp_image_path):
    raise Exception(f"Temporary file not found: {temp_image_path}")

# Define the folder where images should be saved
save_folder = r"C:\Projects\FrameTVAutomation\Images"  # Use raw string for Windows paths
if not os.path.exists(save_folder):
    os.makedirs(save_folder)

# Create a unique filename using the current timestamp
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
filename = f"generated_image_{timestamp}.webp"
destination_path = os.path.join(save_folder, filename)

# Copy the image from the temporary location to your desired folder
shutil.copy(temp_image_path, destination_path)
print("Image saved locally at:", destination_path)
