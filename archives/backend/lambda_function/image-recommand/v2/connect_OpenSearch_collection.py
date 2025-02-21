"""
This script is used to connect to the Amazon OpenSearch Serverless collection.
"""
import boto3
from opensearchpy import OpenSearch, RequestsHttpConnection, AWSV4SignerAuth
import os

HOST = os.environ.get("HOST") # OpenSearch endpoint. For example, abcdefghi.us-east-1.aoss.amazonaws.com (without https://)
REGION = "us-west-2"
service = 'aoss'

def initialize_opensearch_client():
    """
    param: None
    return: OpenSearch client object
    exception: None
    description: Initialize OpenSearch client
    """
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