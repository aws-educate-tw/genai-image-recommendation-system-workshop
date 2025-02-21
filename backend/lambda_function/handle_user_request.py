"""
This script is used to handle user's text input and image input.
"""
from backend.lambda_function.__create_image_embeddings import create_image_embedding, create_word_embedding
import requests
import base64
import os
from PIL import Image
import re


def sanitize_s3_key(image_name):
    """
    param: image_name: image name
    return: image name
    exception: None
    description: Sanitize name (object key) of the image that uploaded by user to S3

    **Note: for workshop purpose, we do not store the new uploaded image to S3 bucket**
    """
    return re.sub(r'[^a-zA-Z0-9_.-]', '_', image_name)

def download_image(url):
    """
    param: url: image URL
    return: image data (bytes)
    exception: None
    description: Download image from URL
    """
    response = requests.get(url)
    if response.status_code == 200:
        return response.content
    else:
        print("Failed to download image!")
        return None

def encode_image_to_base64(image_data):
    """
    param: image_data: image data in bytes
    return: base64 encoded image
    exception: None
    description: Encode image to base64
    """
    return base64.b64encode(image_data).decode('utf-8')


def handle_user_input_image(user_input):
    """
    param: user_input: image URL or key word
    return: object_embedding: The top-5 most similar images
    exception: None
    description: Handle user input image
    """

    # judge the user_input is URL or key word
    if user_input.startswith("http://") or user_input.startswith("https://"):
        image_data = download_image(user_input)
        object_embedding = None
        
        if image_data:
            encoded_image = encode_image_to_base64(image_data)            
            object_embedding = create_image_embedding(image=encoded_image)
    else:
        object_embedding = create_word_embedding(user_input)

    return object_embedding