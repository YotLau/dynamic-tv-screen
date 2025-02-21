import os
import requests
from dotenv import load_dotenv

# Load environment variables at the start
load_dotenv()

class PromptGenerator:

        
    def generate_prompt(self):
        # Check for required environment variables
        required_vars = ['OPENROUTER_API_KEY', 'OPENROUTER_MODEL']
        missing_vars = [var for var in required_vars if not os.getenv(var)]
        
        if missing_vars:
            print(f"Error: Missing required environment variables: {', '.join(missing_vars)}")
            return None

        prompts = [os.getenv(f'PROMPT_{i}') for i in range(1, 9) if os.getenv(f'PROMPT_{i}')]
        
        try:
            response = requests.post(
                os.getenv('OPENROUTER_ENDPOINT'),
                headers={
                    "Authorization": "Bearer " + os.getenv('OPENROUTER_API_KEY'),
                    "Content-Type": "application/json"
                },
                json={
                    "model": os.getenv('OPENROUTER_MODEL'),
                    "messages": [
                        {
                            "role": "system",
                            "content": "You are a wallpaper specialist and artist, look at this list of possible wallpaper prompts. Provide one of your own that keeps the essence of the original prompts in terms of realistic and artistic photography. Provide only the prompt itself without any intro at all."
                        },
                        {
                            "role": "user",
                            "content": ' '.join(prompts)
                        }
                    ]
                }
            )
            response.raise_for_status()
            data = response.json()
            content = data.get('choices', [{}])[0].get('message', {}).get('content')
            print(f"\nRaw content: {content}")
            prompt = content.strip() if content else None
            if prompt:
                print(f"\nGenerated prompt: {prompt}\n")
            return prompt
                
        except Exception:
            return None 