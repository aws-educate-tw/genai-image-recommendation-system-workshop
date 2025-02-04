# Import required library to iterate through dataset
import tqdm as tq
from connect_OpenSearch_collection import initialize_opensearch_client
from create_image_embeddings import embed_images

# ingest your embeddings and the associated image key for each vector 
INDEX_NAME = "image_vectors"
VECTOR_NAME = "vectors"
VECTOR_MAPPING = "image_file"


def ingest_embeddings():
    # Initialize OpenSearch client
    client = initialize_opensearch_client()
    final_embeddings_dataset = embed_images()
    # Ingest embeddings into vector index with associate vector and text mapping fields
    for idx, record in tq.tqdm(final_embeddings_dataset.iterrows(), total=len(final_embeddings_dataset)):
        print(f"Indexing record {idx}, vector_name: {record['image_embedding']}, vector_mapping: {record['image_key']}")
        body = {
            VECTOR_NAME: record['image_embedding'],
            VECTOR_MAPPING: record['image_key']
        }
        response = client.index(index=INDEX_NAME, body=body)

