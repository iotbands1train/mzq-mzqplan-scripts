import boto3

# AWS S3 Configuration
s3_client = boto3.client('s3', region_name='us-west-1')
# Define bucket name and file path
bucket_name = 'mzq-mzqplan-s3bucket'
file_key = 'mzqplan-aws-cloud/d_drive/wrapper_codes/Wrap+Portal+Login+Generator_3.xlsm'
# List objects in the bucket to find the correct key
response = s3_client.list_objects_v2(Bucket=bucket_name, Prefix='mzqplan-aws-cloud/d_drive/wrapper_codes/')
for obj in response.get('Contents', []):
    print(obj['Key'])
