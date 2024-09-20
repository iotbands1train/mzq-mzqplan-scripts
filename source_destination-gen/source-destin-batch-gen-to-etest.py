import boto3
import os
from botocore.exceptions import NoCredentialsError

# AWS S3 client initialization
s3 = boto3.client('s3')

# Define the source and destination
source_dir = r"C:\Users\Administrator\Box\001-MZQ Compliance Services\_Wrapper\Generated Wraps"
bucket_name = "mzq-mzqplan-s3bucket"
destination_dir = "mzqplan-aws-cloud/e_drive/test/"

def upload_to_s3(file_name, bucket, object_name=None):
    try:
        if object_name is None:
            object_name = file_name
        s3.upload_file(file_name, bucket, object_name)
        print(f"File {file_name} uploaded to {bucket}/{object_name}")
    except NoCredentialsError:
        print("Credentials not available")

def sync_directory_to_s3(source_dir, bucket_name, destination_dir):
    for root, dirs, files in os.walk(source_dir):
        for file in files:
            file_path = os.path.join(root, file)
            s3_path = os.path.join(destination_dir, os.path.relpath(file_path, source_dir))
            upload_to_s3(file_path, bucket_name, s3_path.replace("\\", "/"))

if __name__ == "__main__":
    sync_directory_to_s3(source_dir, bucket_name, destination_dir)
