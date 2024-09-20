import os
import hashlib
import boto3
import pandas as pd
from botocore.exceptions import NoCredentialsError

def get_etag_from_client_name(file_name, df):
    """
    Retrieves the ETag based on the client name from the provided DataFrame.

    Parameters:
    file_name (str): The name of the file to match.
    df (DataFrame): The DataFrame containing the client information.

    Returns:
    str or None: The client name (ETag) if a match is found; otherwise, None.
    """
    # Extract the code from the file name
    code = os.path.basename(file_name).split('.')[0]
    
    # Find the matching client name in the DataFrame
    client_name_row = df[df['Code'] == code]
    
    if not client_name_row.empty:
        return client_name_row.iloc[0]['Client Name']
    else:
        return None

def upload_to_s3(local_file, bucket, s3_file):
    """
    Uploads a file to an S3 bucket.

    Parameters:
    local_file (str): The path to the local file to upload.
    bucket (str): The name of the S3 bucket.
    s3_file (str): The path in the S3 bucket where the file will be uploaded.

    Exceptions:
    Prints an error message if the file is not found or if credentials are not available.
    """
    try:
        s3.upload_file(local_file, bucket, s3_file)
        print(f"Upload Successful: {local_file} to {s3_file}")
    except FileNotFoundError:
        print(f"File not found: {local_file}")
    except NoCredentialsError:
        print("Credentials not available")

def sync_folders(local_folder, s3_folder, df):
    """
    Synchronizes the local directory with the S3 bucket based on ETag match.

    Parameters:
    local_folder (str): The path to the local directory to synchronize.
    s3_folder (str): The S3 bucket path to synchronize with.
    df (DataFrame): The DataFrame containing the client information.

    Process:
    - Iterates through the rows of the DataFrame.
    - For each row, constructs the folder path using the 'Code' column.
    - If the folder exists, iterates through the files in the folder.
    - Compares the ETag of each file with the client name.
    - If the ETag matches, uploads the file to the S3 bucket.
    - Prints a message if the ETag does not match or if the file does not exist.
    """
    s3 = boto3.client('s3')
    bucket_name = s3_folder.split('/')[2]
    s3_path_prefix = '/'.join(s3_folder.split('/')[3:])
    
    for _, row in df.iterrows():
        client_name = row['Client Name']
        code = row['Code']
        folder_path = os.path.join(local_folder, code)
        
        if os.path.exists(folder_path) and os.path.isdir(folder_path):
            for root, dirs, files in os.walk(folder_path):
                for file in files:
                    local_file_path = os.path.join(root, file)
                    file_etag = get_etag_from_client_name(local_file_path, df)
                    
                    if file_etag == client_name:
                        relative_path = os.path.relpath(local_file_path, local_folder)
                        s3_file_path = os.path.join(s3_path_prefix, relative_path).replace("\\", "/")
                        upload_to_s3(local_file_path, bucket_name, s3_file_path)
                    else:
                        print(f"ETag mismatch for file: {local_file_path}")

# Load the Excel file with the appropriate encoding
excel_path = 'E:/projcode/excel/Wrap Portal Login Generator_3.xlsm'
df = pd.read_excel(excel_path)

# Define the local and S3 folder paths
local_folder = 'E:/test'
s3_folder = 's3://mzq-mzqplan-s3bucket/mzqplan-aws-cloud/e_drive/test'

# Sync the folders based on ETag match
sync_folders(local_folder, s3_folder, df)
