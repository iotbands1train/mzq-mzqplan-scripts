import os
import boto3
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timedelta

# Initialize S3 client
s3_client = boto3.client('s3')

# Define source and destination
source = r"C:\Users\Administrator\Box\001-MZQ Compliance Services"
bucket_name = "mzq-mzqplan-s3bucket"
bucket_path = "mzqplan-aws-cloud/c_drive/Box/001-MZQ Compliance Services"

# Get yesterday and today dates
yesterday = (datetime.now() - timedelta(days=1)).date()
today = datetime.now().date()

def should_sync(file):
    last_modified = datetime.fromtimestamp(os.path.getmtime(file)).date()
    return last_modified == yesterday or last_modified == today

def upload_file(file):
    try:
        relative_path = os.path.relpath(file, source)
        s3_path = os.path.join(bucket_path, relative_path).replace("\\", "/")
        s3_client.upload_file(file, bucket_name, s3_path, ExtraArgs={'StorageClass': 'STANDARD_IA'})
        print(f"Synced {file} to s3://{bucket_name}/{s3_path}")
    except Exception as e:
        print(f"Failed to sync {file}: {str(e)}")

def get_files_to_sync():
    files_to_sync = []
    for root, dirs, files in os.walk(source):
        for file in files:
            file_path = os.path.join(root, file)
            if should_sync(file_path):
                files_to_sync.append(file_path)
    return files_to_sync

def sync_files_concurrently(files):
    with ThreadPoolExecutor(max_workers=80) as executor:
        future_to_file = {executor.submit(upload_file, file): file for file in files}
        for future in as_completed(future_to_file):
            file = future_to_file[future]
            try:
                future.result()
            except Exception as e:
                print(f"Error syncing file {file}: {e}")

if __name__ == "__main__":
    files_to_sync = get_files_to_sync()
    if files_to_sync:
        print(f"Found {len(files_to_sync)} files to sync.")
        sync_files_concurrently(files_to_sync)
        print("Syncing completed.")
    else:
        print("No files found to sync.")
