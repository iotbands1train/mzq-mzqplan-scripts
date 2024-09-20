import os
import time
from datetime import datetime
import boto3
from concurrent.futures import ThreadPoolExecutor
from boto3.s3.transfer import TransferConfig
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize S3 client with a higher number of connections
s3 = boto3.client('s3', config=boto3.session.Config(max_pool_connections=500))

# Define the S3 transfer configuration with maximum concurrency
config = TransferConfig(
    multipart_threshold=8 * 1024 * 1024,  # 8MB threshold for multipart uploads
    max_concurrency=50,  # Significantly increased number of threads for faster uploads
    multipart_chunksize=2 * 1024 * 1024,  # Smaller chunks for more concurrent uploads
    use_threads=True  # Enable multithreading
)

# Global progress variables
total_files = 0
files_uploaded = 0

def upload_file(local_path, bucket, s3_path):
    global files_uploaded
    try:
        s3.upload_file(local_path, bucket, s3_path, Config=config)
        files_uploaded += 1
        logger.info(f"Successfully uploaded {local_path} to {s3_path} ({files_uploaded}/{total_files})")
    except Exception as e:
        logger.error(f"Failed to upload {local_path} to {s3_path}: {e}")

def sync_directories(local_directory, bucket, s3_directory, max_workers=500):
    global total_files
    upload_tasks = []
    start_time = time.time()  # Start the timer

    # Calculate today's date for comparison
    today = datetime.now().date()

    # Calculate total number of files modified today
    for root, dirs, files in os.walk(local_directory):
        for file in files:
            file_path = os.path.join(root, file)
            file_mod_time = datetime.fromtimestamp(os.path.getmtime(file_path)).date()
            if file_mod_time == today:
                total_files += 1

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        for root, dirs, files in os.walk(local_directory):
            for file in files:
                file_path = os.path.join(root, file)
                file_mod_time = datetime.fromtimestamp(os.path.getmtime(file_path)).date()
                if file_mod_time == today:  # Only process files modified today
                    relative_path = os.path.relpath(file_path, local_directory)
                    s3_path = os.path.join(s3_directory, relative_path).replace("\\", "/")

                    # Schedule the upload
                    upload_tasks.append(executor.submit(upload_file, file_path, bucket, s3_path))

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

    # Sync the directories with increased speed and progress tracking, only syncing files modified today
    sync_directories(local_directory, bucket, s3_directory, max_workers=500)
