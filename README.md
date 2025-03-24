# Dynamic TV Screen

Transform your Samsung Frame TV into an AI-powered art gallery. This application automatically generates unique artistic content using multiple AI models and displays it on your TV, creating an ever-changing exhibition of original artwork.

## Features

- 🎨 AI-powered art generation using Ideogram and DALL-E
- 🤖 Smart prompt generation with Gemini AI
- 📺 Samsung Frame TV integration
- 🔄 Automatic art rotation
- 📁 Local image management
- ⚡ Multiple AI model fallbacks
- 🎯 Customizable negative prompts
- 🌐 Web interface for configuration and control
- 📱 Android app support (in development)

## Prerequisites

- Samsung Frame TV
- Python 3.8+
- Node.js and npm (for web interface)
- API keys for:
  - Ideogram AI
  - OpenRouter (Gemini AI)
- Samsung TV on the same network

## Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/dynamic-tv-screen.git
cd dynamic-tv-screen

# Create and activate virtual environment
python -m venv venv
venv\Scripts\activate  # On Windows
# source venv/bin/activate  # On Unix/MacOS

# Install Python dependencies
pip install -r requirements.txt

# Install frontend dependencies
npm install

# Set up environment variables
copy .env.example .env  # On Windows
# cp .env.example .env  # On Unix/MacOS
```

## Configuration

1. Configure your `.env` file with:
```env
# TV Settings
TV_IP=your_tv_ip_address

# AI API Keys
IDEOGRAM_API_KEY=your_key
OPENROUTER_API_KEY=your_key

# Image Settings
IMAGES_FOLDER=path_to_storage
```

2. Customize prompt templates in `.env`:
```env
PROMPT_1=Your custom prompt template
PROMPT_2=Another prompt template
```

## Usage

### Basic Operation

```bash
# Start the application
python main.py
```

### Art Generation Process

1. **Prompt Generation**
   - The system uses Gemini AI to create artistic prompts
   - Prompts are based on templates in `.env`
   - Each prompt is designed for high-quality art generation

2. **Image Creation**
   - Primary generation through Ideogram AI
   - Fallback to DALL-E if needed
   - Automatic quality control using negative prompts

3. **Image Management**
   - Images automatically saved to configured folder
   - Metadata stored for each generation
   - Automatic cleanup of temporary files

4. **TV Display**
   - Direct integration with Samsung Frame TV
   - Automatic aspect ratio optimization
   - Support for scheduled rotations

## File Structure

```
dynamic-tv-screen/
├── main.py              # Main application entry
├── image_generator.py   # AI image generation logic
├── prompt_generator.py  # AI prompt generation
├── tv_pusher.py        # TV integration
├── config.py           # Configuration management
└── images/             # Generated artwork storage
```

## Troubleshooting

- **TV Connection Issues**
  - Verify TV IP address in `.env`
  - Ensure TV is in Art Mode
  - Check network connectivity

- **Image Generation Failed**
  - Verify API keys
  - Check rate limits
  - Review prompt templates

- **Storage Issues**
  - Ensure write permissions
  - Check available disk space
  - Verify path in IMAGES_FOLDER

## Contributing

Contributions welcome! Please check our contributing guidelines.

## License

MIT License - feel free to use and modify for your needs.