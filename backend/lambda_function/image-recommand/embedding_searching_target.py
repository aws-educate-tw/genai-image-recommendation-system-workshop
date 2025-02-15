# Import required libraries to draw bounding box on image
from PIL import Image, ImageDraw, ImageFont
from create_image_embeddings import create_image_embedding
import requests
import base64
y
def download_image(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.content
    else:
        print("Failed to download image!")
        return None

# Open the extracted object image file in binary mode
def encode_image_to_base64(image_data):
    return base64.b64encode(image_data).decode('utf-8')

def create_test_image_embedding(image_url):
    # Example image URL
    # "https://media.istockphoto.com/id/169978088/photo/santa-monica-pier-sunset.jpg?s=612x612&w=0&k=20&c=hYdJbZGn9bWvY-wKuOhPpVJ_My3qeiuGhku_xHnkHJw="
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