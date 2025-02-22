"""
This is the Lambda function for the image recommendation system.
"""
import json
from handle_user_request import handle_user_input_image
from reverse_image_search import display_top_k_results
from connect_OpenSearch_collection import initialize_opensearch_client
from retrieve_key_words import retrieve_key_words

def lambda_handler(event, context):
    """
    param: event: API Gateway event
    param: context: Lambda context
    return: dict: API Gateway response
    exception: None
    description: 
        This is the entry point for the Lambda function. 
        First, it handle the request by checking the request is from browser or not. If it is from browser, it will return the CORS headers. 
        Then, it will extract the search image from the request body and pass it to the image recommendation system. 
        Finally, it will return the search results to the browser.
    """
    
    if "requestContext" in event and "httpMethod" in event["requestContext"]:
        http_method = event["requestContext"].get("httpMethod")  # 若無則預設為 POST
    else:
        http_method = "POST"  # 直接 Lambda 觸發時

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
        
        body = event.get('body', '{}') 
        if body == "{}":
            search_image = event.get('search_image') 
        else:
            body_json = json.loads(body)        
            search_image = body_json.get('search_image')

        if search_image:
            similar_images_list = []
            key_word_list = retrieve_key_words(search_image)
            # Search for similar images in OpenSearch
            client = initialize_opensearch_client()
            
            for key_word in key_word_list:
                if key_word == "":
                    continue
                
                # Create image embedding
                embedded_image = handle_user_input_image(key_word)
                result = display_top_k_results(client, embedded_image)
                similar_images_list.extend(result)

            return {
                "statusCode": 200,
                "body": json.dumps({
                    "search_image": search_image,
                    "results": similar_images_list,
                })
            }
    return {
        'statusCode': 400,
        'body': json.dumps({'error': 'search_image not found'})
    }
