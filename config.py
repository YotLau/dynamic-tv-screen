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