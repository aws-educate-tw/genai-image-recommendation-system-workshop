# 呼叫入口
import json
from embedding_searching_target import create_test_image_embedding
from reverse_image_search import display_top_k_results
from connect_OpenSearch_collection import initialize_opensearch_client
import boto3
import base64

def lambda_handler(event, context):
    client = initialize_opensearch_client()
    
    # 從 event 取得 search_image_url，如果未提供則預設為空字串
    search_image_url = event.get("search_image_url", "")
    
    # 產生圖片的嵌入特徵
    embedded_image = create_test_image_embedding(search_image_url)
    
    # 執行搜尋並獲取結果
    similar_images_list, similar_images_key_list = display_top_k_results(client, embedded_image)

    # 從 s3 取得圖片
    BUCKET_NAME = "images-for-0307workshop-test1"
    s3 = boto3.client('s3')
    images = {}
    for key in similar_images_key_list:
        response = s3.get_object(Bucket=BUCKET_NAME, Key=key)
        image_data = response['Body'].read()
        images[key] = base64.b64encode(image_data).decode('utf-8')
    
    return {
        "statusCode": 200,
        "body": json.dumps({
            "search_image_url": search_image_url,
            "results": similar_images_list,
            "images": images
        })
    }
