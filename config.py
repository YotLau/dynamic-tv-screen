import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    REQUIRED_VARS = ['IDEOGRAM_API_KEY', 'IDEOGRAM_MODEL', 'IDEOGRAM_STYLE_TYPE', 'IDEOGRAM_ASPECT_RATIO', 'NEGATIVE_PROMPT', 'IMAGES_FOLDER']
    
    @staticmethod
    def validate_env():
        missing_vars = [var for var in Config.REQUIRED_VARS if not os.getenv(var)]
        if missing_vars:
            raise ValueError(f"Missing required environment variables: {', '.join(missing_vars)}")
    
    @staticmethod
    def get_env(key):
        return os.getenv(key)
    
    @staticmethod
    def set_env(key, value):
        os.environ[key] = value
        # Update the .env file to persist the change
        env_path = os.path.join(os.path.dirname(__file__), '.env')
        try:
            # Read existing .env file
            if os.path.exists(env_path):
                with open(env_path, 'r') as f:
                    lines = f.readlines()
                # Update or add the new value
                found = False
                for i, line in enumerate(lines):
                    if line.startswith(f"{key}="):
                        lines[i] = f"{key}={value}\n"
                        found = True
                        break
                if not found:
                    lines.append(f"{key}={value}\n")
            else:
                lines = [f"{key}={value}\n"]
            
            # Write back to .env file
            with open(env_path, 'w') as f:
                f.writelines(lines)
        except Exception as e:
            print(f"Warning: Could not persist environment variable to .env file: {str(e)}")