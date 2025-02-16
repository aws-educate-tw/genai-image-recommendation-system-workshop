"""
This script is used to upload the image to S3 bucket.
"""
import boto3

def initialize_s3_client():
    """
    param: None
    return: s3 client object
    exception: None
    description: Initialize AWS clients
    """
    s3 = boto3.client('s3')
    return s3

def upload_image_to_s3(bucket_name, image_name, image_data):
    """
    param: bucket_name: S3 bucket name
    param: image_name: image name
    param: image_data: image data
    return: None
    exception: None
    description: Upload image to S3 bucket
    """
    s3 = initialize_s3_client()
    if isinstance(image_data, str):
        image_data = image_data.encode('utf-8')  # 如果是字串，轉換為 bytes
    s3.put_object(Bucket=bucket_name, Key=image_name, Body=image_data)

    return image_name