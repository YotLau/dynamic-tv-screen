import os
import requests
from dotenv import load_dotenv  # Added for .env file support
from prompt_generator import PromptGenerator

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
                            "content": "You are an expert wallpaper artist specializing in realistic and artistic photography. Using the reference prompts provided, generate a single, concise wallpaper prompt that captures the same essence and visual richness. Respond with only the prompt text—do not include any introductions, explanations, or extra commentary."
                        },
                        {
                            "role": "user",
                            "content": "Generate a new wallpaper prompt based on these references:"
                        },
                        {
                            "role": "user",
                            "content": prompts
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

def test_prompt_generation():
    # Load environment variables
    load_dotenv()
    
    # Print environment variables for debugging
    print("\nChecking environment variables:")
    print(f"OPENROUTER_API_KEY exists: {'Yes' if os.getenv('OPENROUTER_API_KEY') else 'No'}")
    print(f"OPENROUTER_MODEL: {os.getenv('OPENROUTER_MODEL')}")
    print(f"OPENROUTER_ENDPOINT: {os.getenv('OPENROUTER_ENDPOINT')}")
    
    # Print available prompts
    print("\nAvailable prompts:")
    for i in range(1, 5):
        prompt = os.getenv(f'PROMPT_{i}')
        if prompt:
            print(f"PROMPT_{i}: {prompt[:50]}...")
    
    print("\nTesting prompt generation:")
    # Create generator instance
    generator = PromptGenerator()
    
    # Try to generate a prompt
    result = generator.generate_prompt()
    
    # Check the result
    if result:
        print("\n=== Success! ===")
        print("Generated prompt:", result)
        return True
    else:
        print("\n=== Failed ===")
        print("Could not generate prompt. Check the error messages above.")
        return False

if __name__ == "__main__":
    test_prompt_generation() 