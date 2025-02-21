"""
This script is used to ingest the image embeddings into Amazon OpenSearch Service.
"""
import tqdm as tq
from create_image_embeddings import embed_images
from opensearchpy import OpenSearch, RequestsHttpConnection, AWSV4SignerAuth
from requests_aws4auth import AWS4Auth
import boto3
import os

INDEX_NAME = os.environ.get("INDEX_NAME")
VECTOR_NAME = os.environ.get("VECTOR_NAME")
VECTOR_MAPPING = os.environ.get("VECTOR_MAPPING")
HOST = os.environ.get("HOST") 

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

def upload_embeddings_to_Amazon_OpenSearch_Serverless(client, vector_name, vector_mapping):
    """
    param: client: OpenSearch client object
           index_name: index number
           vector_name: embedding vector 
           vector_mapping: key word for vector
    return: response
    exception: try upload embeddings to Amazon OpenSearch Serverless
    description: Upload embeddings to Amazon OpenSearch Serverless
    """
    """
    in index() function, the body parameter is a dictionary with the following structure:
    :arg index: Name of the data stream or index to target.
    :arg body: The document
    """
    body = {
        VECTOR_NAME: vector_name,
        VECTOR_MAPPING: vector_mapping
    }
    try:
        response = client.index(index=INDEX_NAME, body=body)
    except Exception as e:
        print(f"Failed to upload embeddings to Amazon OpenSearch Serverless: {e}")
    return response

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
    # tqdm is used to show a progress bar
    # final_embeddings_dataset type: pandas.core.frame.DataFrame
    for idx, record in tq.tqdm(final_embeddings_dataset.iterrows(), total=len(final_embeddings_dataset)):
        print(f"Indexing record {idx}, vector_name: {record['image_embedding']}, vector_mapping: {record['image_key']}")
        response = upload_embeddings_to_Amazon_OpenSearch_Serverless(client, record['image_embedding'], record['image_key'])
        
    print("Ingested embeddings successfully into OpenSearch", response)

if __name__ == "__main__":
    ingest_embeddings()