import os
import boto3
from botocore.exceptions import NoCredentialsError, ClientError
import logging
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger()

# Initialize S3 client
s3_client = boto3.client('s3')

# Set source and destination paths
source_directory = r'Z:\001-MZQ Compliance Services'
bucket_name = 'mzq-mzqplan-s3bucket'
s3_destination = 'mzqplan-aws-cloud/c_drive/Box/001-MZQ Compliance Services/'

# Define the number of workers to max out performance
max_workers = os.cpu_count() * 4  # Aggressive use of threads, can adjust based on testing

def upload_file_to_s3(file_path, bucket, s3_path):
    try:
        s3_client.upload_file(file_path, bucket, s3_path)
        logger.info(f"Uploaded {file_path} to s3://{bucket}/{s3_path}")
    except FileNotFoundError:
        logger.error(f"File {file_path} not found.")
    except NoCredentialsError:
        logger.error("Credentials not available.")
    except ClientError as e:
        logger.error(f"Failed to upload {file_path} to s3://{bucket}/{s3_path}: {e}")

def sync_directory_to_s3(source_dir, bucket, destination, max_workers):
    files_to_upload = []

    for root, dirs, files in os.walk(source_dir):
        for file in files:
            file_path = os.path.join(root, file)
            relative_path = os.path.relpath(file_path, source_dir)
            s3_path = os.path.join(destination, relative_path).replace("\\", "/")
            
            try:
                # Check if file needs to be uploaded
                s3_object = s3_client.head_object(Bucket=bucket, Key=s3_path)
                s3_last_modified = s3_object['LastModified'].timestamp()
                local_last_modified = os.path.getmtime(file_path)
                
                if local_last_modified > s3_last_modified:
                    files_to_upload.append((file_path, bucket, s3_path))
                else:
                    logger.info(f"Skipping {file_path} (not modified since last sync)")
            
            except ClientError as e:
                # If file does not exist in S3, upload it
                if e.response['Error']['Code'] == '404':
                    files_to_upload.append((file_path, bucket, s3_path))
                else:
                    logger.error(f"Error checking {file_path} on S3: {e}")

    # Initialize progress bar
    progress_bar = tqdm(total=len(files_to_upload), desc="Uploading files", unit="file")

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {executor.submit(upload_file_to_s3, file[0], file[1], file[2]): file for file in files_to_upload}
        
        for future in as_completed(futures):
            file = futures[future]
            try:
                future.result()
                progress_bar.update(1)  # Update progress bar
            except Exception as exc:
                logger.error(f"{file[0]} generated an exception: {exc}")
    
    progress_bar.close()

if __name__ == "__main__":
    sync_directory_to_s3(source_directory, bucket_name, s3_destination, max_workers)
