from embedding_searching_target import create_test_image_embedding
from reverse_image_search import display_top_k_results
from connect_OpenSearch_collection import initialize_opensearch_client

if __name__ == "__main__":
    client = initialize_opensearch_client()
    search_image_url = ""
    embedded_image = create_test_image_embedding(search_image_url)
    display_top_k_results(client, embedded_image)