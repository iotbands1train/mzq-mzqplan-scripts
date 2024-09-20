import boto3

# AWS S3 Configuration
s3_client = boto3.client('s3', region_name='us-west-1')

# Define bucket name and prefix to list objects
bucket_name = 'mzq-mzqplan-s3bucket'
prefix = 'mzqplan-aws-cloud/d_drive/wrapper_codes/'

# List objects in the bucket
response = s3_client.list_objects_v2(Bucket=bucket_name, Prefix=prefix)

print("Objects in the specified path:")
if 'Contents' in response:
    for obj in response['Contents']:
        print(obj['Key'])
else:
    print("No objects found in the specified path.")
