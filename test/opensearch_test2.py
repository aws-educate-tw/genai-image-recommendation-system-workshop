import boto3

client = boto3.client('opensearchserverless', region_name='us-west-2')

response = client.create_security_policy(

response = client.list_collections()
print(response)
