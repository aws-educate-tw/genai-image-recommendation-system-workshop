# store these vectors so they can be searched and retrieved efficiently. To do so, we can use a vector database.
import boto3
# Import required libraries to connect to Amazon OpenSearch Serverless connection
from opensearchpy import OpenSearch, RequestsHttpConnection, AWSV4SignerAuth

# Initialize endpoint name constant
HOST = "abc.us-west-2.aoss.amazonaws.com" # OpenSearch endpoint. For example, abcdefghi.us-east-1.aoss.amazonaws.com (without https://)
REGION = "us-west-2" # OpenSearch region
service = 'aoss' # OpenSearch service name

# connect to your Amazon OpenSearch Serverless collection.
def initialize_opensearch_client():
    
    # Initialize and authenticate with the OpenSearch client
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

