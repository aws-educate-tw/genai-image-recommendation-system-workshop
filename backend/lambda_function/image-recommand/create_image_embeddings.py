"""
This script will generate embeddings for all images stored in the S3 bucket. The embeddings will be generated using the Amazon Bedrock Titan Multimodal Embeddings model. The script will resize the images to meet the model requirements and encode the images as base64 strings before generating the embeddings. The embeddings and associated image file names will be stored in a Pandas DataFrame object.
"""
import boto3
import pandas as pd
import base64
import json
from PIL import Image
import io
import os

BUCKET_NAME = os.environ.get("BUCKET_NAME")
BEDROCK_MODEL_ID = "amazon.titan-embed-image-v1"
REGION = "us-west-2"
# Define max width and height for resizing to accommodate Bedrock limits
MAX_WIDTH = 1024  
MAX_HEIGHT = 1024  


def initialize_s3_client():
    """
    param: None
    return: s3 client object
    exception: None
    description: Initialize AWS clients
    """
    s3 = boto3.client('s3')
    return s3

def initialize_bedrock_client():
    """
    param: None
    return: bedrock client object
    exception: None
    description: Initialize AWS clients
    """
    bedrock_client = boto3.client(
        "bedrock-runtime", 
        REGION, 
        endpoint_url=f"https://bedrock-runtime.{REGION}.amazonaws.com"
    )
    return bedrock_client

BEDROCK_CLIENT = initialize_bedrock_client()
S3 = initialize_s3_client()

def retrieve_images_from_s3():
    """
    param: None
    return: list of objects in S3 bucket
    exception: None
    description: Retrieve images stored in S3 bucket, including subfolders
    """
    global BUCKET_NAME, S3
    response = S3.list_objects_v2(Bucket=BUCKET_NAME)
    contents = response.get('Contents', [])
    return contents

def resize_image(image_data):
    """
    param: image_data: image data in bytes
    return: resized image in bytes
    exception: None
    description: Resize image while maintaining aspect ratio
    """
    image = Image.open(io.BytesIO(image_data))

    # Resize image while maintaining aspect ratio
    image.thumbnail((MAX_WIDTH, MAX_HEIGHT))

    # Save resized image to bytes buffer
    buffer = io.BytesIO()
    image.save(buffer, format="JPEG")
    buffer.seek(0)

    return buffer.read()

def create_word_embedding(word):
    """
    param: word: word
    return: embedding value
    exception: None
    description: Generate word embedding using Amazon Bedrock Titan Multimodal Embeddings model
    """
    global BEDROCK_CLIENT, BEDROCK_MODEL_ID
    word_input = {}

    if word is not None:
        word_input["inputText"] = word
    else:
        raise ValueError("Word input is required")

    word_body = json.dumps(word_input)

    # Invoke Amazon Bedrock with encoded word body
    bedrock_response = BEDROCK_CLIENT.invoke_model(
        body=word_body,
        modelId=BEDROCK_MODEL_ID,
        accept="application/json",
        contentType="application/json"
    )

    # Retrieve body in JSON response
    final_response = json.loads(bedrock_response.get("body").read())

    embedding_error = final_response.get("message")

    if embedding_error is not None:
        print (f"Error creating embeddings: {embedding_error}")

    # Return embedding value
    return final_response.get("embedding")

def create_image_embedding(image):
    """
    param: image: base64 encoded image
    return: embedding value
    exception: None
    description: Generate image embedding using Amazon Bedrock Titan Multimodal Embeddings model
    """
    global BEDROCK_CLIENT, BEDROCK_MODEL_ID
    image_input = {}

    if image is not None:
        image_input["inputImage"] = image
    else:
        raise ValueError("Image input is required")

    image_body = json.dumps(image_input)

    # Invoke Amazon Bedrock with encoded image body
    bedrock_response = BEDROCK_CLIENT.invoke_model(
        body=image_body,
        modelId=BEDROCK_MODEL_ID,
        accept="application/json",
        contentType="application/json"
    )

    # Retrieve body in JSON response
    final_response = json.loads(bedrock_response.get("body").read())

    embedding_error = final_response.get("message")

    if embedding_error is not None:
        print (f"Error creating embeddings: {embedding_error}")

    # Return embedding value
    return final_response.get("embedding")

def embed_images(image_data):
    """
    param: image_data: image data in bytes
    return: image_embedding: image embedding
    exception: None
    description: Generate image embedding for input image data
    """
    # Resize the image to meet model requirements
    resized_image = resize_image(image_data)

    # Create base64 encoded image for Titan Multimodal Embeddings model input
    base64_encoded_image = base64.b64encode(resized_image).decode('utf-8')

    # Generate the embedding for the resized image
    image_embedding = create_image_embedding(image=base64_encoded_image)
    return image_embedding
    
    
def embed_images_from_s3():
    """
    param: None
    return: final_embeddings_dataset: Pandas DataFrame object
    exception: None
    description: Generate embeddings for all images stored in S3 bucket
    """
    global BUCKET_NAME
    contents = retrieve_images_from_s3()
    
    # Define arrays to hold embeddings and image file key names
    image_embeddings = []
    image_file_names = []

    # Loop through S3 bucket to encode each image, generate its embedding, and append to array
    for obj in contents:
        image_data = S3.get_object(Bucket=BUCKET_NAME, Key=obj['Key'])['Body'].read()
        print(f"Generating embedding for image: {obj['Key']}")
        print(f"Image size: {len(image_data)} bytes")
        image_embeddings.append(embed_images(image_data))
        image_file_names.append(obj["Key"])

    print("Embeddings generated for all images in S3 bucket")

    # Add and list embeddings with associated image file key to dataframe object
    final_embeddings_dataset = pd.DataFrame({'image_key': image_file_names, 'image_embedding': image_embeddings})
    print(final_embeddings_dataset.head())
    return final_embeddings_dataset

def embed_image_for_new_image_in_s3(image_key):
    """
    param: image_key: image key
    return: image_embedding: image embedding
    exception: None
    description: Generate embedding for a specific image stored in S3 bucket
    """
    global BUCKET_NAME
    image_data = S3.get_object(Bucket=BUCKET_NAME, Key=image_key)['Body'].read()

    final_embeddings_dataset = pd.DataFrame({'image_key': [image_key], 'image_embedding': [embed_images(image_data)]})
    print(f"Generating embedding for image: {image_key}")
    print(f"Image size: {len(image_data)} bytes")
    return final_embeddings_dataset


if __name__ == "__main__":
    embed_images_from_s3()