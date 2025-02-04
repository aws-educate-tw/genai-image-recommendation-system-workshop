import boto3


bucket_name = 'images-for-0307workshop-test1'
knowledgebase_name = 'knowledge-base-quick-start-b9641'

def initialize_bedrock_client():
    # 初始化Bedrock客戶端
    bedrock = boto3.client('bedrock', region_name='us-west-2')
    return bedrock

def create_knowledgebase(bedrock, knowledgebase_name):
    global bucket_name
    # 創建知識庫
    # bedrock.create_knowledgebase(
    #     KnowledgebaseName=knowledgebase_name
    # )
    response = bedrock.create_knowledge_base(
        KnowledgeBaseName='MyMultiModalKnowledgeBase',
        DataSource={
            'S3': {
                'Bucket': bucket_name,
                'Key': 'dataset.zip'
            }
        }
    )
    return response

def generate_embeddings(bedrock):
    # 嵌入知識庫
    # bedrock.embed_knowledgebase(
    #     KnowledgebaseName=knowledgebase_name
    # )
    embedding_response = bedrock.invoke_model(
        ModelId='amazon.titan.embeddings',
        Body={
            'Input': {
                'Text': 'example query text',
                'Images': ['url_to_image']
            }
        }
    )
    embeddings = embedding_response['Output']
    return embeddings


def generate_rag(bedrock, embeddings):
    # 生成RAG
    # bedrock.generate_rag(
    #     KnowledgebaseName=knowledgebase_name
    # )
    query_response = bedrock.invoke_model(
        ModelId='amazon.titan.chat',
        Body={
            'Input': {
                'Query': 'What is in the image?',
                'Embeddings': embeddings
            }
        }
    )
    response_text = query_response['Output']['Text']
    print(response_text)
    return response_text


