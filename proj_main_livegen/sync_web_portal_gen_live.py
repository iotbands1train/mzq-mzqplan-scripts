import boto3
import os

# AWS S3 Configuration
s3_client = boto3.client('s3', region_name='us-west-1')

# Define local file path and S3 bucket details
local_file_path = r'C:\Users\Administrator\Box\001-MZQ Compliance Services\_Wrapper\Wrap Portal Login Generator_3.xlsm'
bucket_name = 'mzq-mzqplan-s3bucket'
s3_file_key = 'mzqplan-aws-cloud/d_drive/wrapper_codes/Wrap Portal Login Generator_3.xlsm'

def upload_file_to_s3(local_file, bucket, key):
    try:
        s3_client.upload_file(local_file, bucket, key)
        print(f'Successfully uploaded {local_file} to s3://{bucket}/{key}')
    except Exception as e:
        print(f'Error uploading file: {e}')

if os.path.exists(local_file_path):
    upload_file_to_s3(local_file_path, bucket_name, s3_file_key)
else:
    print(f'File {local_file_path} does not exist.')
