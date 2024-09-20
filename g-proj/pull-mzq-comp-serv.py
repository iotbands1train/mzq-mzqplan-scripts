import boto3
import os
import time
from botocore.exceptions import NoCredentialsError, ClientError
from concurrent.futures import ThreadPoolExecutor

# Initialize the S3 client with Transfer Config
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

# Function to recursively sync an S3 directory with a local directory using multithreading
def sync_directories(bucket, s3_directory, local_directory, max_workers=10):
    paginator = s3.get_paginator('list_objects_v2')
    download_tasks = []
    
    # Start timing the sync process
    start_time = time.time()
    
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        for page in paginator.paginate(Bucket=bucket, Prefix=s3_directory):
            for obj in page.get('Contents', []):
                s3_path = obj['Key']
                relative_path = os.path.relpath(s3_path, s3_directory)
                local_path = os.path.join(local_directory, relative_path).replace("/", "\\")
                
                # Schedule the download
                download_tasks.append(executor.submit(download_file, bucket, s3_path, local_path))
        
        # Ensure all downloads are completed
        for task in download_tasks:
            task.result()

    # End timing and print the duration
    end_time = time.time()
    duration = end_time - start_time
    print(f"Sync completed in {duration:.2f} seconds")

# Define your S3 bucket, S3 path, and local directory
bucket = "mzq-mzqplan-s3bucket"
s3_directory = "mzqplan-aws-cloud/c_drive/Box/001-MZQ Compliance Services"
local_directory = r"E:\001-MZQ Compliance Services"

# Sync the directories with increased speed
sync_directories(bucket, s3_directory, local_directory, max_workers=40)
