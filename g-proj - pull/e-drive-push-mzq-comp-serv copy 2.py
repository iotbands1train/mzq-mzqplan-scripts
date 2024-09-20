import json
import boto3
import os
import time
from concurrent.futures import ThreadPoolExecutor
from boto3.s3.transfer import TransferConfig
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize S3 client with a moderate number of connections
s3 = boto3.client('s3', config=boto3.session.Config(max_pool_connections=150))

# Define the S3 transfer configuration with moderate settings
config = TransferConfig(
    multipart_threshold=8 * 1024 * 1024,  # 8MB threshold for multipart uploads
    max_concurrency=10,  # Reduced number of threads to avoid crashes
    multipart_chunksize=8 * 1024 * 1024,  # Size of each part for multipart uploads
    use_threads=True  # Enable multithreading
)

def file_exists_in_s3(bucket, s3_path):
    try:
        s3.head_object(Bucket=bucket, Key=s3_path)
        return True
    except s3.exceptions.ClientError as e:
        if e.response['Error']['Code'] == '404':
            return False
        else:
            logger.error(f"Error checking {s3_path} in S3: {e}")
            raise

def upload_file(local_path, bucket, s3_path):
    try:
        if not file_exists_in_s3(bucket, s3_path):
            s3.upload_file(local_path, bucket, s3_path, Config=config)
            logger.info(f"Successfully uploaded {local_path} to {s3_path}")
        else:
            logger.info(f"File {s3_path} already exists in S3, skipping upload")
    except Exception as e:
        logger.error(f"Failed to upload {local_path} to {s3_path}: {e}")

def sync_directories(local_directory, bucket, s3_directory, max_workers=10):
    upload_tasks = []
    start_time = time.time()  # Start the timer

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        for root, dirs, files in os.walk(local_directory):
            for file in files:
                local_path = os.path.join(root, file)
                relative_path = os.path.relpath(local_path, local_directory)
                s3_path = os.path.join(s3_directory, relative_path).replace("\\", "/")
                
                # Schedule the upload
                upload_tasks.append(executor.submit(upload_file, local_path, bucket, s3_path))

    # Ensure all uploads are completed
    for task in upload_tasks:
        task.result()

    end_time = time.time()  # End the timer
    elapsed_time = end_time - start_time  # Calculate elapsed time in seconds
    
    # Convert to minutes and hours
    elapsed_minutes = elapsed_time / 60
    elapsed_hours = elapsed_time / 3600

    logger.info(f"All files uploaded successfully in {elapsed_time:.2f} seconds")
    logger.info(f"Time elapsed: {elapsed_minutes:.2f} minutes ({elapsed_hours:.2f} hours)")

# Ensure proper multiprocessing on Windows
if __name__ == "__main__":
    # Define your local directory, bucket name, and S3 path
    local_directory = r"C:\Users\Administrator\Box\001-MZQ Compliance Services\_Wrapper\Generated Wraps"
    bucket = "mzq-mzqplan-s3bucket"
    s3_directory = "mzqplan-aws-cloud/e_drive/test"

    # Sync the directories with moderate speed
    sync_directories(local_directory, bucket, s3_directory, max_workers=50)
