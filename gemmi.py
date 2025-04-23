#!/usr/bin/env python3
"""
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
    The script generates images based on user-provided prompts and saves them

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
"""

import logging
import os
import re
import sys
from io import BytesIO
from dotenv import load_dotenv
from PIL import Image
from google import genai
from google.genai import types

# ------------------------------------------------------------------------------
# Configuration: target banner size
# ------------------------------------------------------------------------------
BANNER_WIDTH = 1200
BANNER_HEIGHT = 628

# ------------------------------------------------------------------------------
# Logging Configuration
# ------------------------------------------------------------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger(__name__)


class GeminiImageGenerator:
    """
    A class to interact with the Gemini API for image generation.
    """

    def __init__(self, api_key: str, model_name: str = "gemini-2.0-flash-exp-image-generation"):
        try:
            self.client = genai.Client(api_key=api_key)
            self.model_name = model_name
            logger.info("Initialized GeminiImageGenerator with model: %s", model_name)
        except Exception as e:
            logger.exception("Failed to initialize Gemini client: %s", e)
            raise

    def generate_image(self, prompt: str) -> Image.Image:
        """
        Sends the prompt to Gemini and returns a PIL Image.
        """
        try:
            logger.info("Sending image generation request with prompt: %s", prompt)
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=prompt,
                config=types.GenerateContentConfig(response_modalities=["Text", "Image"])
            )
            logger.info("Received response from Gemini API.")

            for part in response.candidates[0].content.parts:
                if part.inline_data is not None:
                    img = Image.open(BytesIO(part.inline_data.data))
                    logger.info("Image generated successfully (original size: %sx%s).",
                                img.width, img.height)
                    return img

            raise ValueError("No image data found in API response.")

        except Exception as e:
            logger.exception("Error during image generation: %s", e)
            raise

    def save_image(self, image: Image.Image, filename: str):
        """
        Saves the image into the 'images/' directory.
        """
        try:
            images_dir = "images"
            os.makedirs(images_dir, exist_ok=True)
            path = os.path.join(images_dir, filename)
            image.save(path)
            logger.info("Image saved to %s (%sx%s)", path, image.width, image.height)
        except Exception as e:
            logger.exception("Failed to save image: %s", e)
            raise


def next_image_filename(directory: str = "images", prefix: str = "img", ext: str = ".png") -> str:
    """
    Scans `directory` for existing files like 'img<number>.png' and returns
    the next filename in sequence.
    """
    os.makedirs(directory, exist_ok=True)
    pattern = re.compile(rf"^{re.escape(prefix)}(\d+){re.escape(ext)}$")
    max_index = 0

    for fname in os.listdir(directory):
        m = pattern.match(fname)
        if m:
            idx = int(m.group(1))
            max_index = max(max_index, idx)

    next_index = max_index + 1
    return f"{prefix}{next_index}{ext}"


if __name__ == "__main__":
    # 1) Load API key
    load_dotenv("GEMINI_API_KEY.env")
    API_KEY = os.getenv("GEMINI_API_KEY")
    if not API_KEY:
        logger.error("GEMINI_API_KEY not found in GEMINI_API_KEY.env. Please add it and try again.")
        sys.exit(1)

    # 2) Multi-line prompt input
    print("Enter your image prompt (finish by entering an empty line):")
    lines = []
    while True:
        line = input()
        if not line:
            break
        lines.append(line)
    prompt = "\n".join(lines).strip()
    if not prompt:
        logger.error("No prompt provided; exiting.")
        sys.exit(1)

    try:
        print("Generating image…")
        gen = GeminiImageGenerator(api_key=API_KEY)
        image = gen.generate_image(prompt)

        # 3) Force to banner size, preserving aspect by stretching
        image = image.resize((BANNER_WIDTH, BANNER_HEIGHT), Image.LANCZOS)
        logger.info("Resized image to fixed banner size: %sx%s", BANNER_WIDTH, BANNER_HEIGHT)

        # 4) Save with next sequential filename
        filename = next_image_filename()
        gen.save_image(image, filename)

        print(f"Saved as {filename} ({BANNER_WIDTH}×{BANNER_HEIGHT})")

    except Exception as e:
        logger.error("Image generation process failed: %s", e)
        sys.exit(1)
