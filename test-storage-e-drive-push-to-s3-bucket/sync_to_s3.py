import os
import boto3
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm

def upload_file_to_s3(file_path, bucket_name, s3_path):
    """Upload a single file to S3."""
    s3 = boto3.client('s3')
    try:
        s3.upload_file(file_path, bucket_name, s3_path)
        print(f"Uploaded: {file_path} to s3://{bucket_name}/{s3_path}")
    except Exception as e:
        print(f"Error uploading {file_path} to s3://{bucket_name}/{s3_path}: {e}")

def get_all_files(source_path):
    """Get all files in the source directory."""
    file_paths = []
    for dirpath, _, filenames in os.walk(source_path):
        for filename in filenames:
            file_paths.append(os.path.join(dirpath, filename))
    return file_paths

def main():
    source_path = r"E:\\"
    bucket_name = "mzq-mzqplan-s3bucket"
    destination_path = "mzqplan-aws-cloud/e_drive/"

    # Get all files to upload
    files = get_all_files(source_path)
    
    # Upload files with progress bar
    with ThreadPoolExecutor(max_workers=40) as executor:
        futures = []
        for file in files:
            s3_file_path = os.path.relpath(file, source_path).replace("\\", "/")
            s3_full_path = os.path.join(destination_path, s3_file_path)
            futures.append(executor.submit(upload_file_to_s3, file, bucket_name, s3_full_path))
        
        # Use tqdm for progress tracking
        for _ in tqdm(as_completed(futures), total=len(futures), desc="Uploading files", unit="file"):
            pass

    print("File upload to S3 completed!")

if __name__ == "__main__":
    main()
