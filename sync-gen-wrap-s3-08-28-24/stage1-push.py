import boto3
import os
from botocore.exceptions import NoCredentialsError, ClientError
from concurrent.futures import ThreadPoolExecutor

# Initialize the S3 client
s3 = boto3.client('s3')

# Function to check if a file exists in S3
def file_exists_in_s3(bucket, s3_path):
    try:
        s3.head_object(Bucket=bucket, Key=s3_path)
        return True
    except ClientError:
        return False

# Function to upload a file to S3
def upload_file(file_name, bucket, s3_path):
    try:
        s3.upload_file(file_name, bucket, s3_path)
        print(f'Successfully uploaded {file_name} to {s3_path}')
    except FileNotFoundError:
        print(f'The file {file_name} was not found')
    except NoCredentialsError:
        print('Credentials not available')
    except ClientError as e:
        print(f'Error occurred: {e}')

# Function to recursively sync a local directory with an S3 bucket using multithreading (Exact Sync)
def sync_directories_exact(local_directory, bucket, s3_directory, max_workers=60):
    upload_tasks = []
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        for root, dirs, files in os.walk(local_directory):
            for file in files:
                local_path = os.path.join(root, file)
                relative_path = os.path.relpath(local_path, local_directory)
                s3_path = os.path.join(s3_directory, relative_path).replace("\\", "/")
                
                # Check if the file already exists in S3
                if not file_exists_in_s3(bucket, s3_path):
                    # Schedule the upload if it doesn't exist in S3
                    upload_tasks.append(executor.submit(upload_file, local_path, bucket, s3_path))
                else:
                    print(f'Skipping {file} as it already exists in S3')
        
        # Ensure all uploads are completed
        for task in upload_tasks:
            task.result()

# Define your local directory, bucket name, and S3 path
local_directory = r"C:\Users\Administrator\Box\001-MZQ Compliance Services\_Wrapper\Generated Wraps"
bucket = "mzq-mzqplan-s3bucket"
s3_directory = "mzqplan-aws-cloud/c_drive/Box/001-MZQ Compliance Services/_Wrapper/Generated Wraps"

# Sync the directories with exact match check
sync_directories_exact(local_directory, bucket, s3_directory, max_workers=300)
