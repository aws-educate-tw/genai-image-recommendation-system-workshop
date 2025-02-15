"""
This is the Lambda function for the image recommendation system.
"""
import json
from embedding_searching_target import create_test_image_embedding
from reverse_image_search import display_top_k_results
from connect_OpenSearch_collection import initialize_opensearch_client
import boto3
import base64

def lambda_handler(event, context):
    """
    param: event: API Gateway event
    return: response: API Gateway response
    exception: None
    description: Lambda function for image recommendation system
    """
    client = initialize_opensearch_client()
    # print(json.dumps(event)) 
    # print("Event:", json.dumps(event, indent=2))

    http_method = event["requestContext"]["http"]["method"]

    # Due to the preflight request, we need to handle the OPTIONS method
    # preflight request means that the browser is checking if the server allows a certain request
    # CORS (Cross-Origin Resource Sharing) is a security feature implemented in browsers that restricts websites from making requests to a different domain than the one that served the original web page
    if http_method == "OPTIONS":
        return {
            "statusCode": 200,
            "headers": {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "OPTIONS, POST, GET",
                "Access-Control-Allow-Headers": "Content-Type, Authorization"
            },
            "body": ""
        }
    else:
        body = event.get('body')          
        body_json = json.loads(body)        
        search_image_url = body_json.get('search_image_url')

        if search_image_url:
            # Create image embedding
            embedded_image = create_test_image_embedding(search_image_url)

            # Search for similar images in OpenSearch
            similar_images_list, similar_images_key_list = display_top_k_results(client, embedded_image)

            # Retrieve images from S3 bucket
            BUCKET_NAME = "images-for-0307workshop-test1"
            s3 = boto3.client('s3')
            images = {}
            for key in similar_images_key_list:
                response = s3.get_object(Bucket=BUCKET_NAME, Key=key)
                image_data = response['Body'].read()
                images[key] = base64.b64encode(image_data).decode('utf-8')
            
            return {
                "statusCode": 200,
                "body": json.dumps({
                    "search_image_url": search_image_url,
                    "results": similar_images_list,
                    "images": images
                })
            }
    return {
        'statusCode': 400,
        'body': json.dumps({'error': 'search_image_url not found'})
    }
