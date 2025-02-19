from PIL import Image
import os

def combine_images(logo_path, background_path, output_path):
    try:
        # Open the images
        logo = Image.open(logo_path)
        background = Image.open(background_path)
        
        # Check if logo is PNG
        if logo.format != 'PNG':
            raise ValueError("Logo must be a PNG file")
        
        # Get dimensions
        logo_width, logo_height = logo.size
        bg_width, bg_height = background.size
        
        # Calculate new width as 40% of background width
        new_width = int(bg_width * 0.4)
        # Calculate new height maintaining aspect ratio
        aspect_ratio = logo_height / logo_width
        new_height = int(new_width * aspect_ratio)
        
        # Resize logo
        logo = logo.resize((new_width, new_height), Image.LANCZOS)
        logo_width, logo_height = logo.size
        
        # Calculate center position
        x_center = (bg_width - logo_width) // 2
        y_center = (bg_height - logo_height) // 2
        
        # Create a copy of background to paste logo onto
        result = background.copy()
        
        # Paste logo onto background
        # Using logo as mask to preserve transparency
        result.paste(logo, (x_center, y_center), logo)
        
        # Save as JPG
        result = result.convert('RGB')  # Convert to RGB for JPG
        result.save(output_path, 'JPEG', quality=95)
        
        print(f"Successfully created combined image: {output_path}")
        
    except Exception as e:
        print(f"An error occurred: {str(e)}")

# Example usage
if __name__ == "__main__":
    logo_path = r"C:\Users\Yotam Laufman\Desktop\yozmalogoonoback.PNG"
    background_path = r"C:\Projects\FrameTVAutomation\Images\generated_image_20250216_142253.webp"
    output_path = r"C:\Users\Yotam Laufman\Desktop\combined.jpg"
    
    combine_images(r"C:\Users\Yotam Laufman\Desktop\yozmalogoonoback.PNG", 
                   r"C:\Projects\FrameTVAutomation\Images\generated_image_20250216_142253.webp", 
                   r"C:\Users\Yotam Laufman\Desktop\combined.jpg")