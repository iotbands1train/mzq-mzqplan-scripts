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

def download_file(bucket, s3_path, local_path):
    try:
        # Ensure the local directory exists
        if not os.path.exists(os.path.dirname(local_path)):
            os.makedirs(os.path.dirname(local_path))

        s3.download_file(bucket, s3_path, local_path, Config=config)
        logger.info(f"Successfully downloaded {s3_path} to {local_path}")
    except Exception as e:
        logger.error(f"Failed to download {s3_path} to {local_path}: {e}")

def sync_from_s3_to_local(bucket, s3_directory, local_directory, max_workers=10):
    download_tasks = []
    start_time = time.time()  # Start the timer

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        paginator = s3.get_paginator('list_objects_v2')
        for page in paginator.paginate(Bucket=bucket, Prefix=s3_directory):
            for obj in page.get('Contents', []):
                s3_path = obj['Key']
                relative_path = os.path.relpath(s3_path, s3_directory)
                local_path = os.path.join(local_directory, relative_path).replace("/", "\\")

                # Check if the file needs to be downloaded
                if not os.path.exists(local_path) or \
                        obj['LastModified'].timestamp() > os.path.getmtime(local_path):
                    # Schedule the download
                    download_tasks.append(executor.submit(download_file, bucket, s3_path, local_path))

    # Ensure all downloads are completed
    for task in download_tasks:
        task.result()

    end_time = time.time()  # End the timer
    elapsed_time = end_time - start_time  # Calculate elapsed time in seconds
    
    # Convert to minutes and hours
    elapsed_minutes = elapsed_time / 60
    elapsed_hours = elapsed_time / 3600

    logger.info(f"All files downloaded successfully in {elapsed_time:.2f} seconds")
    logger.info(f"Time elapsed: {elapsed_minutes:.2f} minutes ({elapsed_hours:.2f} hours)")

# Ensure proper multiprocessing on Windows
if __name__ == "__main__":
    # Define your bucket name, S3 path, and local directory
    bucket = "mzq-mzqplan-s3bucket"
    s3_directory = "mzqplan-aws-cloud/c_drive/Box/001-MZQ Compliance Services/_Wrapper/Generated Wraps"
    local_directory = r"E:\test"

    # Sync the directories with moderate speed
    sync_from_s3_to_local(bucket, s3_directory, local_directory, max_workers=50)
