#!/usr/bin/env python3
import os
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from config import Config
from logger import setup_logger
from image_generator import generate_image_api
from image_fetcher import fetch_image
from tv_pusher import push_image_to_tv

class ImageGeneratorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("TV Image Generator")
        self.root.geometry("900x800")
        self.logger = setup_logger()
        
        # Configure style
        self.style = ttk.Style()
        self.style.configure('Modern.TFrame', background='#1e3a8a')
        self.style.configure('Modern.TLabelframe', background='#1e3a8a')
        self.style.configure('Modern.TLabelframe.Label', background='#1e3a8a', foreground='white', font=('Segoe UI', 11, 'bold'))
        self.style.configure('Modern.TLabel', background='#1e3a8a', foreground='white', font=('Segoe UI', 10))
        # Updated button styling with darker colors
        self.style.configure('Modern.TButton', 
            background='#1e3a8a',  # Darker blue
            foreground='white', 
            font=('Segoe UI', 10, 'bold'), 
            padding=10)
        self.style.map('Modern.TButton',
            background=[('active', '#1e40af'), ('disabled', '#475569')],  # Darker active and disabled states
            foreground=[('disabled', '#cbd5e1')])
        self.style.configure('Modern.TButton', background='#3b82f6', foreground='white', font=('Segoe UI', 10, 'bold'), padding=10)
        self.style.map('Modern.TButton',
            background=[('active', '#2563eb'), ('disabled', '#64748b')],
            foreground=[('disabled', '#e2e8f0')])
        
        self.setup_ui()

    def setup_ui(self):
        # Main container
        main_frame = ttk.Frame(self.root, padding="20", style='Modern.TFrame')
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Status frame
        status_frame = ttk.LabelFrame(main_frame, text="Status", padding="10", style='Modern.TLabelframe')
        status_frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=10)
        self.status_label = ttk.Label(status_frame, text="Ready", style='Modern.TLabel')
        self.status_label.grid(row=0, column=0, sticky=tk.W)

        # Prompt frame
        prompt_frame = ttk.LabelFrame(main_frame, text="Current Prompt", padding="10", style='Modern.TLabelframe')
        prompt_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=10)
        self.prompt_text = tk.Text(prompt_frame, height=3, wrap=tk.WORD, font=('Helvetica', 10))
        self.prompt_text.grid(row=0, column=0, sticky=(tk.W, tk.E))
        self.prompt_text.insert('1.0', Config.get_env('PROMPT') or 'No prompt configured')
        self.prompt_text.config(bg='#1e40af', fg='white')

        # Image preview frame
        preview_frame = ttk.LabelFrame(main_frame, text="Image Preview", padding="10", style='Modern.TLabelframe')
        preview_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=10)
        self.preview_label = ttk.Label(preview_frame, text="No image generated yet", style='Modern.TLabel')
        self.preview_label.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Buttons frame
        button_frame = ttk.Frame(main_frame, style='Modern.TFrame')
        button_frame.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=10)

        # Generate Prompt button
        self.generate_prompt_button = ttk.Button(button_frame, text="Generate Prompt", command=self.generate_prompt, style='Modern.TButton')
        self.generate_prompt_button.grid(row=0, column=0, padx=10)

        # Generate button
        self.generate_button = ttk.Button(button_frame, text="Generate Image", command=self.generate_image, style='Modern.TButton')
        self.generate_button.grid(row=0, column=1, padx=10)

        # Push to TV button
        self.push_button = ttk.Button(button_frame, text="Push to TV", command=self.push_to_tv, state=tk.DISABLED, style='Modern.TButton')
        self.push_button.grid(row=0, column=2, padx=10)

        # Progress bar
        self.style.configure("Modern.Horizontal.TProgressbar", background='#3b82f6', troughcolor='#1e40af')
        self.progress = ttk.Progressbar(main_frame, mode='indeterminate', style="Modern.Horizontal.TProgressbar")
        self.progress.grid(row=4, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=10)

        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(2, weight=1)
        
        # Configure window background
        self.root.configure(bg='#1e3a8a')

        # Configure grid weights
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(1, weight=1)

    def update_status(self, message):
        self.status_label.config(text=message)
        self.root.update()

    def show_preview(self, image_path):
        try:
            # Open and resize image for preview
            image = Image.open(image_path)
            image.thumbnail((400, 400))  # Resize for preview
            photo = ImageTk.PhotoImage(image)
            self.preview_label.config(image=photo)
            self.preview_label.image = photo  # Keep a reference
        except Exception as e:
            self.logger.error(f"Error showing preview: {str(e)}")

    def generate_prompt(self):
        try:
            self.generate_prompt_button.config(state=tk.DISABLED)
            self.progress.start()
            self.update_status("Generating prompt...")

            # Create instance of PromptGenerator and call generate_prompt
            from prompt_generator import PromptGenerator
            generator = PromptGenerator()
            new_prompt = generator.generate_prompt()

            if new_prompt:
                # Update the prompt text box
                self.prompt_text.config(state=tk.NORMAL)
                self.prompt_text.delete('1.0', tk.END)
                self.prompt_text.insert('1.0', new_prompt)
                self.update_status("Prompt generated successfully!")
            else:
                self.update_status("Failed to generate prompt")

        except Exception as e:
            self.logger.error(f"Error: {str(e)}")
            self.update_status(f"Error generating prompt: {str(e)}")
        finally:
            self.progress.stop()
            self.generate_prompt_button.config(state=tk.NORMAL)

    def generate_image(self):
        try:
            self.generate_button.config(state=tk.DISABLED)
            self.progress.start()
            self.update_status("Generating image...")

            # Validate environment
            Config.validate_env()
            
            # Generate and process image
            temp_image_path = generate_image_api()
            if not temp_image_path or not os.path.exists(temp_image_path):
                raise Exception("Failed to generate image")

            self.update_status("Saving image...")
            self.saved_image_path = fetch_image(temp_image_path, Config.get_env('IMAGES_FOLDER'))
            
            # Show preview and enable push button
            self.show_preview(self.saved_image_path)
            self.push_button.config(state=tk.NORMAL)
            self.update_status("Image generated successfully!")

            # Cleanup temporary file
            if os.path.exists(temp_image_path):
                os.remove(temp_image_path)

        except Exception as e:
            self.logger.error(f"Error: {str(e)}")
            self.update_status(f"Error: {str(e)}")
        finally:
            self.progress.stop()
            self.generate_button.config(state=tk.NORMAL)

    def push_to_tv(self):
        try:
            self.push_button.config(state=tk.DISABLED)
            self.progress.start()
            self.update_status("Pushing image to TV...")

            push_image_to_tv(self.saved_image_path)
            self.update_status("Image successfully pushed to TV!")

        except Exception as e:
            self.logger.error(f"Error: {str(e)}")
            self.update_status(f"Error pushing to TV: {str(e)}")
        finally:
            self.progress.stop()
            self.push_button.config(state=tk.NORMAL)

def main():
    root = tk.Tk()
    app = ImageGeneratorGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()