import os
import requests
from dotenv import load_dotenv

# Load environment variables at the start
load_dotenv()

class PromptGenerator:

        
    def generate_prompt(self):
        try:
            # Check for required environment variables
            required_vars = ['OPENROUTER_API_KEY', 'OPENROUTER_MODEL', 'OPENROUTER_ENDPOINT']
            missing_vars = [var for var in required_vars if not os.getenv(var)]
            
            if missing_vars:
                print(f"Error: Missing required environment variables: {', '.join(missing_vars)}")
                return None

            prompts = [os.getenv(f'PROMPT_{i}') for i in range(1, 5) if os.getenv(f'PROMPT_{i}')]
            print(f"Found {len(prompts)} prompts")
            
            endpoint = os.getenv('OPENROUTER_ENDPOINT')
            api_key = os.getenv('OPENROUTER_API_KEY')
            model = os.getenv('OPENROUTER_MODEL')
            
            print(f"Making request to: {endpoint}")
            print(f"Using model: {model}")
            
            response = requests.post(
                endpoint,
                headers={
                    "Authorization": f"Bearer {api_key}",
                    "Content-Type": "application/json",
                    "HTTP-Referer": "https://github.com/",
                    "X-Title": "Wallpaper Generator"
                },
                json={
                    "model": model,
                    "messages": [
                        {
                            "role": "user",
                            "content": "You are a wallpaper specialist and artist. Generate a new wallpaper prompt that keeps the essence of of realistic and artistic photography made with a professional camera capturing a beautiful and picturesque scene or landscape. Provide only the prompt itself without any intro or explanations. here's a list of prompts to get inspired from: "+
                            "1. A breathtaking coral reef teeming with colorful fish and vibrant corals in crystal-clear turquoise water. Sunlight filters through the water, creating a serene underwater paradise. Captured in photorealistic digital art, with a focus on macro details of marine life. \n\n " +
                            "2. A spectacular sunset over a tropical beach with golden hues reflecting on gentle waves. Tall palm trees frame the scene, and the sky is painted with vibrant colors, creating a serene atmosphere. Rendered in 4K photograph style, viewed from aerial perspective.\n\n " + 
                            "3. A misty forest at dawn with towering trees and soft light filtering through the canopy. The path is lined with wildflowers, and the air is filled with morning dew. Illustrated in ultra-realistic 3D render, capturing a wide forest vista.\n\n " + 
                            "4. A majestic mountain range with snow-capped peaks under a clear blue sky. A tranquil alpine lake reflects the landscape, with evergreen trees in the foreground. Depicted in panoramic photograph, from the perspective of a hiker on a trail.\n\n " + 
                            "5. A serene autumn landscape featuring a calm lake surrounded by trees in vibrant red foliage. A rustic wooden pier extends into the still water, reflecting the stunning colors of fall. The scene is bathed in soft morning light, evoking a sense of peace. Styled as a high-definition digital image, captured from the edge of the pier.\n\n " + 
                            "6. A vast desert landscape under a clear, starry night sky. The rolling dunes are bathed in moonlight, with a solitary camel caravan adding a sense of scale. The scene conveys tranquility, portrayed in detailed panoramic photo, viewed from a distant vantage point.\n\n " + 
                            "7. A mesmerizing aurora borealis illuminating the night sky over a snow-covered landscape. The vibrant greens and purples of the northern lights dance gracefully above, reflecting off a frozen lake. The scene exudes a magical atmosphere, rendered in realistic oil painting, from the perspective of a person gazing up.\n\n " + 
                            "8. A sprawling sunflower field stretching towards the horizon under a bright, clear blue sky. The golden petals of the sunflowers bask in the sunlight, creating a joyful ambiance. Captured in high-resolution photograph, from an elevated viewpoint showcasing the entire field."
                        }
                    ]
                }
            )
            
            if response.status_code != 200:
                print(f"Error response (Status {response.status_code}): {response.text}")
                return None
                
            data = response.json()
            print(f"API Response: {data}")
            
            if not data or 'choices' not in data:
                print("Invalid response format from API")
                return None
                
            content = data['choices'][0]['message']['content'].strip()
            if content:
                print(f"\nGenerated prompt: {content}\n")
                return content
            else:
                print("No content in API response")
                return None
                
        except Exception as e:
            print(f"Exception in generate_prompt: {str(e)}")
            return None 