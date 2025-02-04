# 呼叫入口
import json
from embedding_searching_target import create_test_image_embedding
from reverse_image_search import display_top_k_results
from connect_OpenSearch_collection import initialize_opensearch_client

def lambda_handler(event, context):
    client = initialize_opensearch_client()
    
    # 從 event 取得 search_image_url，如果未提供則預設為空字串
    search_image_url = event.get("search_image_url", "")
    
    # 產生圖片的嵌入特徵
    embedded_image = create_test_image_embedding(search_image_url)
    
    # 執行搜尋並獲取結果
    similar_images_list = display_top_k_results(client, embedded_image)
    
    return {
        "statusCode": 200,
        "body": json.dumps({
            "search_image_url": search_image_url,
            "results": similar_images_list
        })
    }
