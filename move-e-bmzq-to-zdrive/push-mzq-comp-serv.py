import boto3
import os
from botocore.exceptions import NoCredentialsError, ClientError
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm

# Initialize the S3 client
s3 = boto3.client('s3')

# Function to upload a file to S3
def upload_file(file_name, bucket, s3_path):
    try:
        s3.upload_file(file_name, bucket, s3_path)
        return f'Successfully uploaded {file_name} to {s3_path}'
    except FileNotFoundError:
        return f'The file {file_name} was not found'
    except NoCredentialsError:
        return 'Credentials not available'
    except ClientError as e:
        return f'Error occurred: {e}'

# Function to recursively sync a local directory with an S3 bucket using multithreading
def sync_directories(local_directory, bucket, s3_directory, max_workers):
    upload_tasks = []
    total_files = 0

    # First, count the total number of files
    for root, dirs, files in os.walk(local_directory):
        total_files += len(files)

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        with tqdm(total=total_files, desc="Syncing files", unit="file") as pbar:
            for root, dirs, files in os.walk(local_directory):
                for file in files:
                    local_path = os.path.join(root, file)
                    relative_path = os.path.relpath(local_path, local_directory)
                    s3_path = os.path.join(s3_directory, relative_path).replace("\\", "/")

                    # Schedule the upload
                    future = executor.submit(upload_file, local_path, bucket, s3_path)
                    upload_tasks.append(future)

            # Ensure all uploads are completed and update progress bar
            for future in as_completed(upload_tasks):
                result = future.result()
                print(result)  # Print the result of each upload
                pbar.update(1)  # Update the progress bar

# Define your local directory, bucket name, and S3 path
local_directory = r"C:\Users\Administrator\Box\001-MZQ Compliance Services"
bucket = "mzq-mzqplan-s3bucket"
s3_directory = "mzqplan-aws-cloud/c_drive/Box/001-MZQ Compliance Services"  # Corrected to be a relative path

# Sync the directories with increased speed and progress tracking
sync_directories(local_directory, bucket, s3_directory, max_workers=200)
