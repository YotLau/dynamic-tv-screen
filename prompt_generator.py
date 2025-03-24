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
                            "role": "system",
                            "content": "You are an expert wallpaper creator specializing in realistic and artistic photography. Your task is to generate a single prompt for image generation that describes a beautiful scene, landscape, or cityscape. Sometimes, be specific with technical details and compositional techniques, offering clear choices. Other times, focus on evocative descriptions of lighting, mood, and overall artistic vision, providing more freedom for interpretation. Aim for variation in each generated prompt. Include 'Professional fine art photography' at the end. Provide only the prompt itself without any intro or explanations."
                        },
                        {
                            "role": "user",
                            "content": "Generate a breathtaking, hyperrealistic wallpaper of a [choose from: [location_adjective] [scene_type] / remote [natural_landscape] / hidden [urban_setting] / vast [open_space]] during [choose from: [time_of_day] / sunrise / sunset / twilight / midday]. The light is [choose from: [light_quality], [more descriptive light phrase like 'golden and diffused' or 'harsh and dramatic']]. This creates a [choose from: [mood], [more descriptive mood like 'a sense of mystery and wonder' or 'vibrant energy']]. Composition follows [choose from: the [composition_technique], emphasizing [compositional_element] through [compositional_method]]. The photograph has a [choose from: [color_palette], a [more descriptive color palette like 'muted earth tones with a pop of vibrant color' or 'a stark monochrome palette with subtle gradations']]. [Optional technical detail: aperture f/[choose from: [aperture_value], let the AI decide], shutter speed [choose from: [shutter_speed_value], let the AI decide], ISO [choose from: [iso_value], let the AI decide] implying [choose from: [lighting_implication], let the AI imply the lighting]]. [Optional descriptive detail about the scene]. Professional fine art photography."
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