# Import required libraries
import boto3
import pandas as pd
import base64
import json
from PIL import Image
import io

# Constants, change to your S3 bucket name and selected AWS region
BUCKET_NAME = "images-for-0307workshop-test1"
BEDROCK_MODEL_ID = "amazon.titan-embed-image-v1"
REGION = "us-west-2"
# Define max width and height for resizing to accommodate Bedrock limits
MAX_WIDTH = 1024  
MAX_HEIGHT = 1024  


def initialize_s3_client():
    # Initialize AWS clients
    s3 = boto3.client('s3')
    return s3

def initialize_bedrock_client():
    bedrock_client = boto3.client(
        "bedrock-runtime", 
        REGION, 
        endpoint_url=f"https://bedrock-runtime.{REGION}.amazonaws.com"
    )
    return bedrock_client

BEDROCK_CLIENT = initialize_bedrock_client()
S3 = initialize_s3_client()

# Retrieve images stored in S3 bucket 
def retrieve_images_from_s3():
    global BUCKET_NAME, S3
    response = S3.list_objects_v2(Bucket=BUCKET_NAME)
    contents = response.get('Contents', [])
    return contents

# Function to resize image
def resize_image(image_data):
    image = Image.open(io.BytesIO(image_data))

    # Resize image while maintaining aspect ratio
    image.thumbnail((MAX_WIDTH, MAX_HEIGHT))

    # Save resized image to bytes buffer
    buffer = io.BytesIO()
    image.save(buffer, format="JPEG")
    buffer.seek(0)

    return buffer.read()

# Function to create embedding from input image
def create_image_embedding(image):
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

# Because you will be performing a search for similar images stored in the S3 bucket, you will also have to store the image file name as metadata for its embedding. Also, because the model expects a base64 encoded image as input, you will have to create an encoded version of the image for the embedding function.
def embed_images():
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

    print("Embeddings generated for all images in S3 bucket")

    # Add and list embeddings with associated image file key to dataframe object
    final_embeddings_dataset = pd.DataFrame({'image_key': image_file_names, 'image_embedding': image_embeddings})
    print(final_embeddings_dataset.head())

    return final_embeddings_dataset

if __name__ == "__main__":
    embed_images()