import os
import requests
from dotenv import load_dotenv  # Added for .env file support

# Load environment variables
load_dotenv()

class PromptGenerator:
    def generate_prompt(self):
        prompts = [os.getenv(f'PROMPT_{i}') for i in range(1, 9) if os.getenv(f'PROMPT_{i}')]
        print("Collected prompts:", prompts)  # Debug line
        
        try:
            api_url = "https://openrouter.ai/api/v1/chat/completions"  # Fixed URL
            api_key = os.getenv('OPENROUTER_API_KEY')
            model = os.getenv('OPENROUTER_MODEL')
            
            print(f"API URL: {api_url}")  # Debug line
            print(f"API Key present: {'yes' if api_key else 'no'}")  # Debug line
            print(f"Model: {model}")  # Debug line
            
            response = requests.post(
                api_url,
                headers={
                    "Authorization": "Bearer " + api_key,
                    "Content-Type": "application/json"
                },
                json={
                    "model": model,
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
            print("API Response:", data)  # Debug line
            
            prompt = data.get('choices', [{}])[0].get('message', {}).get('content', '').strip() if data else None
            if prompt:
                print(f"\nGenerated prompt: {prompt}\n")
            return prompt
                
        except Exception as e:  # Changed to capture and print the error
            print(f"Error occurred: {str(e)}")
            return None 

# Test code
if __name__ == "__main__":
    # Example environment variables (you should put these in a .env file)
    test_prompts = [
        "A serene mountain landscape at sunset",
        "Abstract geometric patterns in pastel colors",
        "Coastal waves crashing against rocky cliffs",
        "Dense forest in morning mist",
        "Urban nightscape with neon lights",
        "Minimalist Japanese garden",
        "Desert dunes at golden hour",
        "Crystal formations in vivid colors"
    ]
    
    # Set test environment variables (now using range 1-9)
    for i, prompt in enumerate(test_prompts, 1):
        os.environ[f'PROMPT_{i}'] = prompt
    
    # Create and test the generator
    generator = PromptGenerator()
    result = generator.generate_prompt()
    
    if result:
        print("Test successful!")
    else:
        print("Test failed - no prompt generated") 