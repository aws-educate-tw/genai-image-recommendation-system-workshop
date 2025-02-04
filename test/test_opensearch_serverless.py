# store these vectors so they can be searched and retrieved efficiently. To do so, we can use a vector database.
import boto3
# Import required libraries to connect to Amazon OpenSearch Serverless connection
from opensearchpy import OpenSearch, RequestsHttpConnection
from requests_aws4auth import AWS4Auth

# Initialize endpoint name constant
HOST = "elax6edg0jahtqnq6dv5.us-west-2.aoss.amazonaws.com" # OpenSearch endpoint. For example, abcdefghi.us-east-1.aoss.amazonaws.com (without https://)
REGION = "us-west-2" # OpenSearch region

# Initialize and authenticate with the OpenSearch client
credentials = boto3.Session().get_credentials()
auth = AWS4Auth(credentials.access_key, credentials.secret_key, REGION, 'aoss', session_token=credentials.token)


client = OpenSearch(
        hosts=[{'host': HOST, 'port': 443}],
        http_auth=auth,
        use_ssl=True,
        verify_certs=True,
        connection_class=RequestsHttpConnection,
        pool_maxsize=300
    )


indices = client.indices.get('*')  # 取得所有索引
print("索引列表：", list(indices.keys()))