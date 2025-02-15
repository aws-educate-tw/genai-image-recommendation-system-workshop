"""
This script is used to connect to the Amazon OpenSearch Serverless collection.
"""
from create_image_embeddings import create_image_embedding
import requests
import base64

def download_image(url):
    """
    param: url: image URL
    return: image data
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

def create_test_image_embedding(image_url):
    """
    param: image_url: image URL
    return: object_embedding: image embedding
    exception: None
    description: Create image embedding
    """
    # need exepction handling for image_url
    if image_url == "":
        image_url = "https://storage.googleapis.com/kaggle-datasets-images/298806/611794/33134a2eb9c0d349fc18ff4183b1ef07/dataset-cover.png?t=2019-08-12-21-16-57"
    image_data = download_image(image_url)
    object_embedding = None
    
    if image_data:
        encoded_image = encode_image_to_base64(image_data)
        
        # Embed the extracted object image
        object_embedding = create_image_embedding(image=encoded_image)
    
        # Print the first few numbers of the embedding followed by ...
        print(f"Image embedding: {object_embedding[:5]} ...")
    
    return object_embedding