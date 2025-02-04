# https://docs.aws.amazon.com/zh_tw/opensearch-service/latest/developerguide/serverless-sdk.html

from opensearchpy import OpenSearch, RequestsHttpConnection, AWSV4SignerAuth
from requests_aws4auth import AWS4Auth
import boto3
import botocore
import time

# Build the client using the default credential configuration.
# You can use the CLI and run 'aws configure' to set access key, secret
# key, and default region.


client = boto3.client('opensearchserverless', region_name='us-west-2') # low-level service client
service = 'aoss'
region = 'us-west-2'
credentials = boto3.Session().get_credentials()
awsauth = AWS4Auth(credentials.access_key, credentials.secret_key,
                   region, service, session_token=credentials.token)
auth = AWSV4SignerAuth(credentials, region, service)



def createEncryptionPolicy(client):
    """Creates an encryption policy that matches all collections beginning with ws-collection-"""
    try:
        response = client.create_security_policy(
            description='Encryption policy for ws-collection collections',
            name='ws-collection-policy',
            policy="""
                {
                    \"Rules\":[
                        {
                            \"ResourceType\":\"collection\",
                            \"Resource\":[
                                \"collection\/ws-collection-*\"
                            ]
                        }
                    ],
                    \"AWSOwnedKey\":true
                }
                """,
            type='encryption'
        )
        print('\nEncryption policy created:')
        print(response)
    except botocore.exceptions.ClientError as error:
        if error.response['Error']['Code'] == 'ConflictException':
            print(
                '[ConflictException] The policy name or rules conflict with an existing policy.')
        else:
            raise error


def createNetworkPolicy(client):
    """Creates a network policy that matches all collections beginning with ws-collection-"""
    try:
        response = client.create_security_policy(
            description='Network policy for ws-collection collections',
            name='ws-collection-policy',
            policy="""
                [{
                    \"Description\":\"Public access for ws-collection collection\",
                    \"Rules\":[
                        {
                            \"ResourceType\":\"dashboard\",
                            \"Resource\":[\"collection\/ws-collection-*\"]
                        },
                        {
                            \"ResourceType\":\"collection\",
                            \"Resource\":[\"collection\/ws-collection-*\"]
                        }
                    ],
                    \"AllowFromPublic\":true
                }]
                """,
            type='network'
        )
        print('\nNetwork policy created:')
        print(response)
    except botocore.exceptions.ClientError as error:
        if error.response['Error']['Code'] == 'ConflictException':
            print(
                '[ConflictException] A network policy with this name already exists.')
        else:
            raise error


def createAccessPolicy(client):
    """Creates a data access policy that matches all collections beginning with ws-collection-"""
    try:
        response = client.create_access_policy(
            description='Data access policy for ws-collection collections',
            name='ws-collection-policy',
            policy="""
                [{
                    \"Rules\":[
                        {
                            \"Resource\":[
                                \"index\/ws-collection-*\/*\"
                            ],
                            \"Permission\":[
                                \"aoss:CreateIndex\",
                                \"aoss:DeleteIndex\",
                                \"aoss:UpdateIndex\",
                                \"aoss:DescribeIndex\",
                                \"aoss:ReadDocument\",
                                \"aoss:WriteDocument\"
                                
                            ],
                            \"ResourceType\": \"index\"
                        },
                        {
                            \"Resource\":[
                                \"collection\/ws-collection-*\"
                            ],
                            \"Permission\":[
                                \"aoss:CreateCollectionItems\"
                            ],
                            \"ResourceType\": \"collection\"
                        }
                    ],
                    \"Principal\":[
                        \"arn:aws:iam::859893468118:role/EC2Admin\",
                        \"arn:aws:iam::859893468118:role/WSParticipantRole\"
                    ]
                }]
                """,
            type='data'
        )
        print('\nAccess policy created:')
        print(response)
    except botocore.exceptions.ClientError as error:
        if error.response['Error']['Code'] == 'ConflictException':
            print(
                '[ConflictException] An access policy with this name already exists.')
        else:
            raise error


def createCollection(client):
    """Creates a collection"""
    try:
        response = client.create_collection(
            name='ws-collection-sitcoms',
            type='VECTORSEARCH' # 'SEARCH'|'TIMESERIES'|'VECTORSEARCH'
        )
        return(response)
    except botocore.exceptions.ClientError as error:
        if error.response['Error']['Code'] == 'ConflictException':
            print(
                '[ConflictException] A collection with this name already exists. Try another name.')
        else:
            raise error


def waitForCollectionCreation(client):
    """Waits for the collection to become active"""
    response = client.batch_get_collection(
        names=['ws-collection-sitcoms'])
    time.sleep(30)
    # Periodically check collection status
    while (response['collectionDetails'][0]['status']) == 'CREATING':
        print('Creating collection...')
        time.sleep(30)
        response = client.batch_get_collection(
            names=['ws-collection-sitcoms'])
    print('\nCollection successfully created:')
    print(response["collectionDetails"])
    # Extract the collection endpoint from the response
    host = (response['collectionDetails'][0]['collectionEndpoint'])
    final_host = host.replace("https://", "")
    # createIndex(final_host)
    # indexData(final_host)
    ingestData(final_host)

def createIndex(host):
    # Build the OpenSearch client
    client = OpenSearch(
        hosts=[{'host': host, 'port': 443}],
        http_auth=awsauth,
        use_ssl=True,
        verify_certs=True,
        connection_class=RequestsHttpConnection,
        timeout=300
    )
    # It can take up to a minute for data access rules to be enforced
    time.sleep(45)

    # Step 2: Define index settings and mappings
    INDEX_NAME = "images_vectors"
    VECTOR_NAME = "vectors"
    VECTOR_DIMENSIONS = 1024  # Set the dimensionality of your vectors

    # Create index


    index_body = {
        'name': INDEX_NAME,
        'settings': {
            'index': {
                'knn': True,  # Enable k-NN search
                'knn.algo_param.ef_search': 512,  # Set ef_search parameter
                'knn.algo_param.ef_construction': 16,  # Set ef_construction parameter
            }
        },
        'mappings': {
            'properties': {
                VECTOR_NAME: {
                    'type': 'knn_vector',  # Specify knn_vector type for vector search
                    'dimension': VECTOR_DIMENSIONS,  # Set the dimensionality of your vectors
                    'method': {
                        'name': 'hnsw',  # Use HNSW algorithm for vector search
                        'engine': 'nmslib',  # Specify the engine to use
                        'parameters': {
                            'm': 24,  # Number of bi-directional links created for each new element during construction
                        }
                    }
                },
                'image_file': {  # Additional field for image file metadata
                    'type': 'text'
                }
            }
        }
    }

    # It can take up to a minute for data access rules to be enforced
    time.sleep(45)
    response = client.indices.create(index=INDEX_NAME, body=index_body)
    print(f"Index creation response: {response}")


def indexData(host):
    """Create an index and add some sample data
    INDEX_NAME = "images_vectors"
    VECTOR_NAME = "vectors"
    VECTOR_MAPPING = "image_file"    
    """
    # Build the OpenSearch client
    client = OpenSearch(
        hosts=[{'host': host, 'port': 443}],
        http_auth=awsauth,
        use_ssl=True,
        verify_certs=True,
        connection_class=RequestsHttpConnection,
        timeout=300
    )
    # It can take up to a minute for data access rules to be enforced
    time.sleep(45)

    # Create index
    response = client.indices.create('images_vectors')
    print('\nCreating index:')
    print(response)

    # Add a document to the index.
    response = client.index(
        index='images_vectors',
        body={
            'title': 'Seinfeld',
            'creator': 'Larry David',
            'year': 1989
        },
        id='1',
    )
    print('\nDocument added:')
    print(response)

def ListIndices(client):
    # 获取所有索引
    indices = client.cat.indices(format='json')  # 返回 JSON 格式的索引信息

    # 打印所有索引的名称
    for index in indices:
        print(index['index'])

# List all 
def ingestData(host):
    # create an opensearch client and use the request-signer
    client = OpenSearch(
        hosts=[{'host': host, 'port': 443}],
        http_auth=auth,
        use_ssl=True,
        verify_certs=True,
        connection_class=RequestsHttpConnection,
        pool_maxsize=20,
    )

    # create an index
    index_name = 'books-index'
    create_response = client.indices.create(
        index_name
    )

    print('\nCreating index:')
    print(create_response)

    # index a document
    document = {
    'title': 'The Green Mile',
    'director': 'Stephen King',
    'year': '1996'
    }

    response = client.index(
        index = 'books-index',
        body = document,
        id = '1'
    )

    time.sleep(20)
    print('\nIndexing document:', response)


    # delete the index
    delete_response = client.indices.delete(
        index_name
    )

    print('\nDeleting index:')
    print(delete_response)


def main():
    createEncryptionPolicy(client)
    createNetworkPolicy(client)
    createAccessPolicy(client)

    createCollection(client)
    waitForCollectionCreation(client)
    # ListIndices(client)


if __name__ == "__main__":
    main()