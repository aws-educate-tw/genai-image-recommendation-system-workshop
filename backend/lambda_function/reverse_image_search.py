"""
This module contains the functions to search the OpenSearch index for similar images
"""
import os
from PIL import Image
from connect_OpenSearch_collection import initialize_opensearch_client
import boto3

client = initialize_opensearch_client()
region = "us-west-2"
INDEX_NAME = "image_vectors"
VECTOR_NAME = "vectors"
VECTOR_MAPPING = "image_files"

def search_index(client, object_embedding):
    """
    param: client: OpenSearch client object
    param: object_embedding: image embedding
    return: list of similar images
    exception: None
    description: Search the OpenSearch index for similar images
    """
    # Define number of images to search and retrieve
    K_SEARCHES = 15

    # Define search configuration body for K-NN 
    body = {
            "size": K_SEARCHES,
            "_source": {
                "exclude": [VECTOR_NAME],
            },
            "query": {
                "knn": {
                    "vectors": {
                        "vector": object_embedding,
                        "k": K_SEARCHES,
                    }
                }
            },
            "_source": True,
            "fields": [VECTOR_MAPPING],
        }

    # Invoke OpenSearch to search through index with K-NN configurations
    # response format: https://opensearch.org/docs/latest/api-reference/search/
    knn_response = client.search(index=INDEX_NAME, body=body)
    
    result = []
    ids = set()  # Set to keep track of already retrieved images and their scores

    # Loop through response to print the closest matching results
    for hit in knn_response["hits"]["hits"]:
        id_ = hit["_id"]
        score = hit["_score"]
        item_id_ = hit["_source"][VECTOR_MAPPING]

        # Check if score has already been tracked, if not, add it to final result
        if id_ not in ids:
            final_item = [item_id_, score]
            print("final_item", final_item)
            result.append(final_item)
            ids.add(id_)  # Log score as tracked already

    # Print Top K closest matches
    print(f"Top {K_SEARCHES} closest embeddings and associated scores: {result}")
    return result

def display_top_k_results(client, object_embedding):
    """
    param: client: OpenSearch client object
    param: object_embedding: image embedding
    return: list of similar images
    exception: None
    description: Display the top K similar images
    """

    similar_images_key_list = [] # List to store similar images' keys
    # List of image file names from the K-NN search
    image_files = search_index(client, object_embedding) 

    # Download and display each image that matches image query
    for file_name in image_files:
        """
        file_name[0] is the file path
        file_name[1] is the score
        """
        print("File Path: " + file_name[0])
        print("Score: " + str(file_name[1]))
        similar_images_key_list.append(file_name[0])

    return similar_images_key_list