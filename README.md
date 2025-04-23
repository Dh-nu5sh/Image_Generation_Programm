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




---------------------------------------------------------------------------------------------------------------------------------------------------

PRO'S:

Single-Prompt Workflow: Accepts a multi-line prompt in one go, letting you describe “10% off” banners with rich detail in a single step.

Automated Sequencing: Auto-increments filenames (img1.png, img2.png…) so you can batch-generate multiple offers without naming headaches.

Consistent Banner Size: Forces every output to a fixed 1200×628 resolution, ensuring uniformity across all marketing assets.

API-Driven Creativity: Leverages Google Gemini’s image model for on-demand, AI-powered design variations from the same prompt.

Robust Logging: Tracks each stage (init, request, resize, save) for easy debugging and audit trails of generated campaigns.

Error Handling & Validation: Graceful checks on API key presence, response content, and file operations to minimize runtime failures.

Environment Configuration: Reads API credentials from a .env file, separating secrets from code and streamlining deployment.

Directory Management: Auto-creates an images/ folder if missing, so you can run it anywhere without manual setup.
