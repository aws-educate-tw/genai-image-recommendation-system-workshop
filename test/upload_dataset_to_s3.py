import boto3

# 初始化S3客戶端
s3 = boto3.client('s3')

# 上傳文件到S3
bucket_name = 'images-for-0307workshop-test1'
file_path = 'src/kaggle/dataset.zip'
s3.upload_file(file_path, 'dataset.zip')
