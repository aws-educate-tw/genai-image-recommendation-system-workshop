"""
This Script is used to upload the React frontend files to s3 bucket. 
This Script will be run in EC2 instance to upload the frontend files generated after npm run build to s3 bucket.
"""
import boto3
import os

BUCKET_NAME = "<your_s3_bucket_name>"
REGION = "<your_region>"
FRONTEND_PATH = "<path_to_frontend_build_files>"

S3 = boto3.client("s3", region_name=REGION)

def upload_files_to_s3():
    """
    param: None
    return: None
    exception: None
    description: Upload frontend files to S3 bucket
    """
    global BUCKET_NAME, S3, FRONTEND_PATH
    for root, dirs, files in os.walk(FRONTEND_PATH):
        for file in files:
            file_path = os.path.join(root, file)
            key = file_path.replace(FRONTEND_PATH, "").lstrip("/")
            if key.endswith(".html"):
                S3.upload_file(file_path, BUCKET_NAME, key, ExtraArgs={"ContentType": "text/html"})
            elif key.endswith(".css"):
                S3.upload_file(file_path, BUCKET_NAME, key, ExtraArgs={"ContentType": "text/css"})
            elif key.endswith(".js"):
                S3.upload_file(file_path, BUCKET_NAME, key, ExtraArgs={"ContentType": "application/javascript"})
            else:
                S3.upload_file(file_path, BUCKET_NAME, key)
            print(f"Uploaded {file_path} to s3://{BUCKET_NAME}/{key}")

if __name__ == "__main__":
    upload_files_to_s3()