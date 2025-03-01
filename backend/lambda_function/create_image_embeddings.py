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

BEDROCK_MODEL_ID = "amazon.titan-embed-image-v1"
REGION = "us-west-2"

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