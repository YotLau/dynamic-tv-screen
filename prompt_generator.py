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
                            "content": "You are an expert wallpaper creator specializing in realistic and artistic photography. Your task is to generate a single prompt for image generation that describes a beautiful scene, landscape, or cityscape. Use a mix of evocative descriptions (lighting, mood, artistic vision) and occasional technical or compositional details to create visually stunning and varied outputs. Ensure each prompt reflects a professional fine art photography style.Provide only the prompt itself without any intro or explanations."
                        },
                        {
                             "role": "user",
                            "content": "[Choose from: Create / Design / Imagine] a [choose from: serene / vibrant / dramatic / peaceful / moody] [choose from: photograph / image / scene] of a [choose from: bustling city street / tranquil forest glade / sunlit coastal village / moonlit desert dune / foggy mountain pass / rainy urban alleyway / futuristic skyline / secluded beach cove]. The light is [choose from: soft and diffused / harsh and dramatic / warm and golden / cool and misty], evoking a sense of [choose from: mystery / wonder / calm / energy]. Composition follows [choose from: the rule of thirds / leading lines / symmetry / negative space], emphasizing [choose from: the horizon / a central subject / depth / balance]. The color palette is [choose from: muted earth tones / vibrant and saturated / cool and calming / warm and inviting]. [Optional: Add a detail like ‘A lone figure stands in the distance’ or ‘Reflections glow on wet pavement’]. Professional fine art photography."
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