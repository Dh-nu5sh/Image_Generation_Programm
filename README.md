# Image_Generation_Programm

gemmi.py

A script to generate images via Google’s Gemini API, saving each
output with a sequential filename (img1.png, img2.png, …), prompting
for a multi-line input at runtime, and forcing every output to a
fixed banner resolution. 
---------------------------------------------------------------------------------------------------------------------------------------------------
Note:
    This script is designed to work with the Google Gemini API and requires
    an API key stored in a file named "GEMINI_API_KEY.env" in the same directory.
    The API key should be set as an environment variable named "GEMINI_API_KEY".
    The script generates images based on user-provided prompts and saves them.

---------------------------------------------------------------------------------------------------------------------------------------------------
Dependencies:
    pip install google-genai pillow python-dotenv

Usage Example:
    $ python generate_image.py
    Enter your image prompt (finish by entering an empty line):
    Create a vibrant digital banner ad for the beverage company Coce.
    Use a rich red background inspired by Thums Up’s signature hue.
    Place a realistic Coce tin can front-and-center with the “Coce” logo.
    
    Generating image…
    Saved as img1.png (1200×628)
