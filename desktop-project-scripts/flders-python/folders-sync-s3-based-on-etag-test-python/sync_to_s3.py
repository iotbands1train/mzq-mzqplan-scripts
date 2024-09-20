import os
import boto3
from botocore.exceptions import NoCredentialsError

def sync_folder_to_s3(local_folder, s3_folder):
    """
    Synchronizes the local folder with the specified S3 bucket folder.

    Parameters:
    local_folder (str): The path to the local directory to synchronize.
    s3_folder (str): The S3 bucket path to synchronize with.

    Process:
    - Iterates through all files in the local directory.
    - Constructs the S3 file path based on the relative path in the local directory.
    - Uploads each file to the specified S3 bucket folder.
    - Prints a success message for each uploaded file.
    - Prints an error message if the file is not found or if credentials are not available.

    Example:
    Given a local folder with files and an S3 folder path:
    - All files in the local folder will be uploaded to the corresponding S3 folder.
    """
    s3 = boto3.client('s3')
    bucket_name = s3_folder.split('/')[2]
    s3_path_prefix = '/'.join(s3_folder.split('/')[3:])
    
    for root, dirs, files in os.walk(local_folder):
        for file in files:
            local_file_path = os.path.join(root, file)
            relative_path = os.path.relpath(local_file_path, local_folder)
            s3_file_path = os.path.join(s3_path_prefix, relative_path).replace("\\", "/")
            
            try:
                s3.upload_file(local_file_path, bucket_name, s3_file_path)
                print(f"Upload Successful: {local_file_path} to {s3_file_path}")
            except FileNotFoundError:
                print(f"File not found: {local_file_path}")
            except NoCredentialsError:
                print("Credentials not available")

# Define the local and S3 folder paths
local_folder = 'E:/test'
s3_folder = 's3://mzq-mzqplan-s3bucket/mzqplan-aws-cloud/e_drive/test'

# Sync the folders
sync_folder_to_s3(local_folder, s3_folder)
