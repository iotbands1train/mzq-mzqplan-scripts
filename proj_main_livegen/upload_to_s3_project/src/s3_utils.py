# Import the boto3 library, which is the AWS SDK for Python
import boto3

def get_s3_client(region_name):
    """
    Creates an S3 client using the specified AWS region.
    
    Args:
    region_name (str): The AWS region where the S3 bucket is located.

    Returns:
    boto3.client: An S3 client object.
    """
    # Create and return an S3 client configured for the specified region
    return boto3.client('s3', region_name=region_name)

def upload_file_to_s3(s3_client, local_file, bucket, key):
    """
    Uploads a local file to an S3 bucket.
    
    Args:
    s3_client (boto3.client): The S3 client object.
    local_file (str): The path to the local file to be uploaded.
    bucket (str): The name of the S3 bucket.
    key (str): The S3 key (path in the bucket) where the file will be stored.

    Returns:
    str: A message indicating the success or failure of the upload.
    """
    try:
        # Attempt to upload the file to the specified S3 bucket with the given key
        s3_client.upload_file(local_file, bucket, key)
        # Return a success message if the upload completes without exception
        return f'Successfully uploaded {local_file} to s3://{bucket}/{key}'
    except Exception as e:
        # Return an error message if an exception occurs during the upload
        return f'Error uploading file: {e}'
