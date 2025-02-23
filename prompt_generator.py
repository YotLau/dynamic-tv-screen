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