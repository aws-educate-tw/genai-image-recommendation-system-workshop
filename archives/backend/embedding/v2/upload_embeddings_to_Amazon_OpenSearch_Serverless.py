"""
This script is used to ingest the image embeddings into Amazon OpenSearch Service.
"""
import tqdm as tq
from create_image_embeddings import embed_images
from opensearchpy import OpenSearch, RequestsHttpConnection, AWSV4SignerAuth
from requests_aws4auth import AWS4Auth
import boto3
import time

INDEX_NAME = "image_vectors"
VECTOR_NAME = "vectors"
VECTOR_MAPPING = "image_file"

def initialize_opensearch_client():
    """
    param: None
    return: OpenSearch client object
    exception: None
    description: Initialize OpenSearch client
    """
    HOST = "ft9k300rv6bp5ul8q6o1.us-west-2.aoss.amazonaws.com" # OpenSearch endpoint. For example, abcdefghi.us-east-1.aoss.amazonaws.com (without https://)
    REGION = "us-west-2" # OpenSearch region
    service = 'aoss' # OpenSearch service name
    
    credentials = boto3.Session().get_credentials()
    auth = AWSV4SignerAuth(credentials, REGION, service)

    client = OpenSearch(
        hosts=[{'host': HOST, 'port': 443}],
        http_auth=auth,
        use_ssl=True,
        verify_certs=True,
        connection_class=RequestsHttpConnection,
        pool_maxsize=300
    )
    return client

def ingest_embeddings():
    """
    param: None
    return: None
    exception: None
    description: Ingest embeddings into OpenSearch
    explanation: This function is used to ingest the image embeddings into Amazon OpenSearch Service.
    vector index with associate vector and text mapping fields
    """
    client = initialize_opensearch_client()
    final_embeddings_dataset = embed_images()

    # Ingest embeddings into vector index with associate vector and text mapping fields
    for idx, record in tq.tqdm(final_embeddings_dataset.iterrows(), total=len(final_embeddings_dataset)):
        print(f"Indexing record {idx}, vector_name: {record['image_embedding']}, vector_mapping: {record['image_key']}")
        """
        in index() function, the body parameter is a dictionary with the following structure:
        :arg index: Name of the data stream or index to target.
        :arg body: The document
        """
        # idx: the index of the record
        body = {
            VECTOR_NAME: record['image_embedding'], # VECTOR_NAME: the embedding vector
            VECTOR_MAPPING: record['image_key'] # VECTOR_MAPPING: the image file path name in S3
        }
        response = client.index(index=INDEX_NAME, body=body)
    print("Ingested embeddings successfully into OpenSearch", response)

if __name__ == "__main__":
    # calculate the running time
    start_time = time.time()
    ingest_embeddings()
    end_time = time.time()
    print(f"Time taken to ingest embeddings: {end_time - start_time} seconds")