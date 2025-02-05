# 呼叫入口
import json
from embedding_searching_target import create_test_image_embedding
from reverse_image_search import display_top_k_results
from connect_OpenSearch_collection import initialize_opensearch_client
import boto3
import base64

def lambda_handler(event, context):
    client = initialize_opensearch_client()
    print(json.dumps(event))  # 可用來查看完整的事件資料
    print("Event:", json.dumps(event, indent=2))

    # 確保 HTTP 方法的取得方式正確
    http_method = event["requestContext"]["http"]["method"]

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
        # 解析body部分（假設body已經是字串格式）
        body = event.get('body')  # 使用get()來避免KeyError
        
        # 將JSON字串轉換為Python字典
        body_json = json.loads(body)
        
        # 從解析後的字典中取得search_image_url
        search_image_url = body_json.get('search_image_url')

        # print(event)
        # # 從 event 取得 search_image_url，如果未提供則預設為空字串
        # search_image_url = event.get("search_image_url", "")
        if search_image_url:
        
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
    return {
        'statusCode': 400,
        'body': json.dumps({'error': 'search_image_url not found'})
    }
