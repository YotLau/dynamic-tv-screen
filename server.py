#!/usr/bin/env python3
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os
from tkinter import Tk, filedialog
from config import Config
from logger import setup_logger
from image_generator import generate_image_api
from image_fetcher import fetch_image
from tv_pusher import push_image_to_tv
from prompt_generator import PromptGenerator

app = Flask(__name__)
# Allow all origins for development
CORS(app, resources={r"/*": {"origins": "*"}})
logger = setup_logger()

# Serve static images
@app.route('/images/<path:filename>')
def serve_image(filename):
    try:
        images_folder = Config.get_env('IMAGES_FOLDER')
        return send_from_directory(images_folder, filename)
    except Exception as e:
        logger.error(f"Error serving image: {str(e)}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/select-folder', methods=['POST'])
def select_folder():
    try:
        # Create a root window but hide it
        root = Tk()
        root.withdraw()

        # Increase timeout and handle dialog asynchronously
        root.after(100, lambda: root.focus_force())
        folder_path = filedialog.askdirectory(parent=root)
        root.destroy()

        if not folder_path:
            return jsonify({'success': False, 'error': 'No folder selected'})

        # Convert to absolute path and normalize
        folder_path = os.path.abspath(folder_path)

        # Ensure the folder exists
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)

        # Update the environment variable and config
        os.environ['IMAGES_FOLDER'] = folder_path
        Config.set_env('IMAGES_FOLDER', folder_path)

        # Log the successful folder selection
        logger.info(f"Selected folder path: {folder_path}")

        return jsonify({
            'success': True,
            'folderPath': folder_path
        })

    except Exception as e:
        logger.error(f"Error selecting folder: {str(e)}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/generate-prompt', methods=['POST'])
def generate_prompt():
    try:
        generator = PromptGenerator()
        new_prompt = generator.generate_prompt()
        if new_prompt:
            return jsonify({'success': True, 'prompt': new_prompt})
        return jsonify({'success': False, 'error': 'Failed to generate prompt'}), 400
    except Exception as e:
        logger.error(f"Error generating prompt: {str(e)}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/generate-image', methods=['POST'])
def generate_image():
    try:
        Config.validate_env()
        data = request.get_json()
        prompt = data.get('prompt')
        
        if not prompt:
            return jsonify({'success': False, 'error': 'No prompt provided'}), 400
            
        image_url = generate_image_api(prompt)
        if not image_url:
            return jsonify({'success': False, 'error': 'Failed to generate image'}), 400

        return jsonify({
            'success': True,
            'imageUrl': image_url
        })

    except Exception as e:
        logger.error(f"Error: {str(e)}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/list-images')
def list_images():
    # This endpoint will return the same data as list-local-images for now
    # since we're storing all images locally
    return list_local_images()

@app.route('/api/list-local-images')
def list_local_images():
    try:
        images_folder = Config.get_env('IMAGES_FOLDER')
        if not os.path.exists(images_folder):
            return jsonify({'success': False, 'error': 'Images folder not found'}), 404
            
        # List all files in the images folder
        image_files = [f for f in os.listdir(images_folder) 
                      if os.path.isfile(os.path.join(images_folder, f)) 
                      and f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.webp'))]
        
        return jsonify({
            'success': True,
            'images': image_files
        })

    except Exception as e:
        logger.error(f"Error listing local images: {str(e)}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/push-to-tv', methods=['POST'])
def push_to_tv():
    try:
        data = request.get_json()
        image_url = data.get('imageUrl')
        tv_ip = data.get('tvIp')
        
        if not image_url:
            return jsonify({'success': False, 'error': 'Invalid image URL'}), 400
            
        if not tv_ip:
            return jsonify({'success': False, 'error': 'TV IP address is required'}), 400

        # If the image URL is a local path (from gallery), use it directly
        if image_url.startswith('/images/'):
            image_path = os.path.join(os.path.dirname(__file__), image_url.lstrip('/'))
        else:
            # Download the image temporarily for TV push
            image_path = fetch_image(image_url, Config.get_env('IMAGES_FOLDER'))

        # Push the image to TV
        push_image_to_tv(image_path, tv_ip)
        
        # Cleanup temporary file only if it was downloaded
        if not image_url.startswith('/images/') and os.path.exists(image_path):
            os.remove(image_path)
            
        return jsonify({'success': True})

    except Exception as e:
        logger.error(f"Error: {str(e)}")
        return jsonify({'success': False, 'error': str(e)}), 500

if __name__ == '__main__':
    try:
        # Ensure the images folder exists
        os.makedirs(Config.get_env('IMAGES_FOLDER'), exist_ok=True)
        # Run the server
        app.run(host='0.0.0.0', port=5000, debug=True)
    except Exception as e:
        logger.error(f"Server startup error: {str(e)}")