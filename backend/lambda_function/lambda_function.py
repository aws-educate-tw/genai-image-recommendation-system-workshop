"""
This is the Lambda function for the image recommendation system.
"""
import json
from handle_user_request import handle_user_input
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
            client = initialize_opensearch_client()
            
            is_text_mode = search_image.startswith("http://") or search_image.startswith("https://")
            results = []
            if is_text_mode:
                key_word_list = retrieve_key_words(search_image)
                top_k = 15
                similar_images_list = []
                for key_word in key_word_list:
                    if key_word == "":
                        continue
                    
                    # Create image embedding
                    embedded_image = handle_user_input(key_word)
                    result = display_top_k_results(client, embedded_image, top_k)
                    similar_images_list.append(result)
                
                for i in range(top_k):
                    for j in range(len(similar_images_list)):
                        if len(similar_images_list[j]) > i and similar_images_list[j][i] not in results:
                            results.append(similar_images_list[j][i])
                    if len(results) >= 20:
                        break
            else:
                embedded_image = handle_user_input(search_image)
                results = display_top_k_results(client, embedded_image, 20)

            return {
                "statusCode": 200,
                "body": json.dumps({
                    "search_image": search_image,
                    "results": results,
                })
            }
    return {
        'statusCode': 400,
        'body': json.dumps({'error': 'search_image not found'})
    }
