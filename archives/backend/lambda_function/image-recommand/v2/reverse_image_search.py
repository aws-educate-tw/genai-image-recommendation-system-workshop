"""
This module contains the functions to search the OpenSearch index for similar images
"""
import os
from PIL import Image
from connect_OpenSearch_collection import initialize_opensearch_client
import boto3

s3 = boto3.client('s3')
client = initialize_opensearch_client()
region = "us-west-2"
INDEX_NAME = "image_vectors"
VECTOR_NAME = "vectors"
VECTOR_MAPPING = "image_file"
BUCKET_NAME = os.environ.get("BUCKET_NAME")

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
    knn_response = client.search(index=INDEX_NAME, body=body)
    result = []
    scores_tracked = set()  # Set to keep track of already retrieved images and their scores

    # Loop through response to print the closest matching results
    for hit in knn_response["hits"]["hits"]:
        id_ = hit["_id"]
        score = hit["_score"]
        item_id_ = hit["_source"][VECTOR_MAPPING]

        # Check if score has already been tracked, if not, add it to final result
        if score not in scores_tracked:
            final_item = [item_id_, score]
            result.append(final_item)
            scores_tracked.add(score)  # Log score as tracked already

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

    similar_images_list = [] # List to store similar images' public URLs
    similar_images_key_list = [] # List to store similar images' keys
    # List of image file names from the K-NN search
    image_files = search_index(client, object_embedding)

    # Create a local directory to store downloaded images
    # download_dir = 'RESULTS'
    download_dir = "/tmp/my_downloads"

    # Create directory if not exists
    os.makedirs(download_dir, exist_ok=True)

    # Download and display each image that matches image query
    for file_name in image_files:
        print("File Path: " + file_name[0])
        print("Score: " + str(file_name[1]))
        file_path = file_name[0]
        file_name = file_path.split("/")[-1]
    
        s3.download_file(Bucket = BUCKET_NAME, Key = file_path, Filename = "/tmp/"+file_name)

        # store the similar images in a list
        # https://<bucket-name>.s3.<region>.amazonaws.com/<key>
        public_url = f"https://{BUCKET_NAME}.s3.{region}.amazonaws.com/{file_path}"
        similar_images_list.append(public_url)
        similar_images_key_list.append(file_path)

    return similar_images_list, similar_images_key_list