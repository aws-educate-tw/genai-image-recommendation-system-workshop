import os
from PIL import Image
from embedding_searching_target import create_test_image_embedding
from connect_OpenSearch_collection import initialize_opensearch_client
import boto3


s3 = boto3.client('s3')
client = initialize_opensearch_client()
VECTOR_NAME = "vectors"
VECTOR_MAPPING = "image_file"
INDEX_NAME = "image_vectors"
BUCKET_NAME = "images-for-0307workshop-test1"

# define the number of results to retrieve from the index and invoke the Amazon OpenSearch Service client with a search request
def search_index(client, object_embedding):
    # Define number of images to search and retrieve
    K_SEARCHES = 3

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
    
# fetch each specific image to display the results
# Function to display image
def display_image(image_path):
    image = Image.open(image_path)
    image.show()

def display_top_k_results(client, object_embedding):
    
    # List of image file names from the K-NN search
    image_files = search_index(client, object_embedding)

    # Create a local directory to store downloaded images
    download_dir = 'RESULTS'

    # Create directory if not exists
    os.makedirs(download_dir, exist_ok=True)

    # Download and display each image that matches image query
    for file_name in image_files:
        print("File Path: " + file_name[0])
        print("Score: " + str(file_name[1]))
        file_path = file_name[0]
        file_name = file_path.split("/")[-1]
        # local_path = os.path.join(download_dir, file_name[0])
        # print(local_path)
        # Ensure to add in the necessary prefix before the file name if files are in subdirectories in the bucket
        # ex. s3.download_file(BUCKET_NAME, "training/loafers/"+file_name[0], local_path)
        s3.download_file(Bucket = BUCKET_NAME, Key = file_path, Filename = file_name)

        # Open downloaded image and display it
        # display_image(local_path)
        print(f"Downloaded image: {file_path}")
        print()

embedded_image = create_test_image_embedding()
display_top_k_results(client, embedded_image)