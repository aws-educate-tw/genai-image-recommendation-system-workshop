"""
This script generates image embeddings for all images in an S3 bucket using the Amazon Bedrock Multimodal Embeddings model.
"""
import boto3
import pandas as pd
import base64
import json
from PIL import Image, ImageFile
import io
import time

BUCKET_NAME = "photo-gallery-bucket-ws0307"
BEDROCK_MODEL_ID = "amazon.titan-embed-image-v1"
REGION = "us-west-2"
ImageFile.LOAD_TRUNCATED_IMAGES = True # Set the flag to avoid PIL error when loading truncated images

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
    image_num = 0
    global BUCKET_NAME, S3
    paginator = S3.get_paginator('list_objects_v2') # Create a paginator object, which allows you to iterate over pages of S3 objects
    contents = []
    for page in paginator.paginate(Bucket=BUCKET_NAME):
        for obj in page.get('Contents', []):
            image_num += 1
            contents.append(obj)
    print(f"Found {image_num} images in S3 bucket")
    time.sleep(2)
    return contents

def resize_image(image_data):
    """
    param: image_data(type: bytes)  
    return: resized image
    exception: None
    description: Resize image while maintaining aspect ratio
    """
    image = Image.open(io.BytesIO(image_data))
    if image.mode != "RGB":
        image = image.convert("RGB")

    # Resize image while maintaining aspect ratio
    image.thumbnail((MAX_WIDTH, MAX_HEIGHT))

    buffer = io.BytesIO()
    image.save(buffer, format="JPEG")
    buffer.seek(0)

    return buffer.read()

def create_image_embedding(image):
    """
    param: image(type: base64 encoded image)
    return: embedding value
    exception: None
    description: Create embedding from input image by invoking multomodal embeddings model in Amazon Bedrock
    """
    global BEDROCK_CLIENT, BEDROCK_MODEL_ID
    image_input = {}

    if image is not None:
        image_input["inputImage"] = image
    else:
        raise ValueError("Image input is required")

    image_body = json.dumps(image_input)
    try:
        bedrock_response = BEDROCK_CLIENT.invoke_model(
            body=image_body,
            modelId=BEDROCK_MODEL_ID,
            accept="application/json",
            contentType="application/json"
        )

        final_response = json.loads(bedrock_response.get("body").read())
        embedding_error = final_response.get("message")
    except Exception as e:
        if e.response['Error']['Code'] in ['ThrottlingException', 'RateLimitExceeded']:
            # Exponential backoff: increase the backoff time on each retry
            print(f"Throttling detected. Retrying in {2} seconds...")
            time.sleep(2)
        else:
            raise e

    if embedding_error is not None:
        print (f"Error creating embeddings: {embedding_error}")

    return final_response.get("embedding")

def embed_images():
    """
    param: None
    return: final_embeddings_dataset
    exception: None
    description: The entry point for the script to generate image embeddings for all images in an S3 bucket
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

        # Resize the image to meet model requirements
        resized_image = resize_image(image_data)

        # Create base64 encoded image for Titan Multimodal Embeddings model input
        base64_encoded_image = base64.b64encode(resized_image).decode('utf-8')

        # Generate the embedding for the resized image
        image_embedding = create_image_embedding(image=base64_encoded_image)
        image_embeddings.append(image_embedding)
        image_file_names.append(obj["Key"])

    # End of loop
    print("Embeddings generated for all images in S3 bucket")

    # Add and list embeddings with associated image file key to dataframe object
    final_embeddings_dataset = pd.DataFrame({'image_key': image_file_names, 'image_embedding': image_embeddings})
    return final_embeddings_dataset
