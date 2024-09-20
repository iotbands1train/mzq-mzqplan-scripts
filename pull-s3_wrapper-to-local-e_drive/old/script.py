import boto3
import os
from botocore.exceptions import NoCredentialsError, ClientError

# Initialize the S3 client
s3 = boto3.client('s3')

# Function to download a file from S3
def download_file(bucket, s3_path, local_path):
    try:
        # Ensure the local directory exists
        if not os.path.exists(os.path.dirname(local_path)):
            os.makedirs(os.path.dirname(local_path))
        s3.download_file(bucket, s3_path, local_path)
        print(f'Successfully downloaded {s3_path} to {local_path}')
    except NoCredentialsError:
        print('Credentials not available')
    except ClientError as e:
        print(f'Error occurred: {e}')
    except OSError as e:
        print(f'OS error: {e}')

# Function to recursively sync an S3 directory with a local directory
def sync_directories(bucket, s3_directory, local_directory):
    paginator = s3.get_paginator('list_objects_v2')
    for page in paginator.paginate(Bucket=bucket, Prefix=s3_directory):
        for obj in page.get('Contents', []):
            s3_path = obj['Key']
            relative_path = os.path.relpath(s3_path, s3_directory)
            local_path = os.path.join(local_directory, relative_path).replace("/", "\\")

            # Download the file
            download_file(bucket, s3_path, local_path)

# Define your S3 bucket, S3 path, and local directory
bucket = "mzq-mzqplan-s3bucket"
s3_directory = "mzqplan-aws-cloud/c_drive/Box/001-MZQ Compliance Services/_Wrapper/Generated Wraps"

local_directory = r"E:\001-MZQ Compliance Services\_Wrapper\Generated Wraps"

# Sync the directories
sync_directories(bucket, s3_directory, local_directory)
