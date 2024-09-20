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

def should_sync(path):
    """Check if the file or folder was modified yesterday or today."""
    last_modified = datetime.fromtimestamp(os.path.getmtime(path)).date()
    return last_modified == yesterday or last_modified == today

def upload_file(file):
    """Upload a single file to S3."""
    try:
        relative_path = os.path.relpath(file, source)
        s3_path = os.path.join(bucket_path, relative_path).replace("\\", "/")
        s3_client.upload_file(file, bucket_name, s3_path, ExtraArgs={'StorageClass': 'STANDARD_IA'})
        print(f"Synced {file} to s3://{bucket_name}/{s3_path}")
    except Exception as e:
        print(f"Failed to sync {file}: {str(e)}")

def get_items_to_sync():
    """Get a list of folders and files that need to be synced."""
    items_to_sync = []
    for root, dirs, files in os.walk(source):
        if should_sync(root):  # Check if the directory was modified
            items_to_sync.append(root)
        for file in files:
            file_path = os.path.join(root, file)
            if should_sync(file_path):  # Check if the file was modified
                items_to_sync.append(file_path)
    return items_to_sync

def sync_files_concurrently(files, max_workers=60):
    """Sync files concurrently to S3."""
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_to_file = {executor.submit(upload_file, file): file for file in files if os.path.isfile(file)}
        for future in as_completed(future_to_file):
            file = future_to_file[future]
            try:
                future.result()
            except Exception as e:
                print(f"Error syncing file {file}: {e}")

if __name__ == "__main__":
    items_to_sync = get_items_to_sync()
    if items_to_sync:
        print(f"Found {len(items_to_sync)} items to sync.")
        sync_files_concurrently(items_to_sync, max_workers=60)  # Adjust max_workers here
        print("Syncing completed.")
    else:
        print("No items found to sync.")
