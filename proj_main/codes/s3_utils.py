import boto3

# AWS S3 Configuration
s3_client = boto3.client('s3', region_name='us-west-1')

def get_s3_etag(bucket, key):
    response = s3_client.head_object(Bucket=bucket, Key=key)
    return response['ETag']

def download_file(bucket, key, local_path):
    s3_client.download_file(bucket, key, local_path)

def upload_file_to_s3(local_file, bucket, key):
    s3_client.upload_file(local_file, bucket, key)
