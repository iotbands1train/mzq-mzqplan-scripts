import os
import boto3
import subprocess

# Define the new source and destination paths
source_s3_path = "s3://mzq-mzqplan-s3bucket/mzqplan-aws-cloud/c_drive/Box/001-MZQ Compliance Services/_Wrapper/Generated Wraps/"
destination_local_path = "E:\\001-MZQ Compliance Services\\_Wrapper\\Generated Wraps"

# Initialize the S3 client
s3_client = boto3.client('s3')

# Configure AWS CLI with optimized settings for maximum performance
aws_configure_commands = [
    "aws configure set default.region us-west-1",  # Set default region
    "aws configure set default.s3.max_concurrent_requests 100",  # Increase the number of concurrent requests
    "aws configure set default.s3.multipart_threshold 32MB",  # Lower the multipart threshold for faster upload start
    "aws configure set default.cli_read_timeout 1200",  # Increase read timeout to handle large files
    "aws configure set default.cli_connect_timeout 1200",  # Increase connect timeout for better reliability
    "aws configure set default.s3.max_bandwidth 0",  # Remove bandwidth limit (0 means no limit)
    "aws configure set default.s3.multipart_chunksize 8MB",  # Reduce chunk size for finer granularity in uploads
    "aws configure set default.s3.max_queue_size 10000"  # Increase the queue size for more requests
]

# Run the AWS CLI configuration commands
for command in aws_configure_commands:
    subprocess.run(command, shell=True, check=True)

# Sync the files from S3 to the local directory
sync_command = f"aws s3 sync {source_s3_path} {destination_local_path} --exact-timestamps"
subprocess.run(sync_command, shell=True, check=True)

print("Sync completed successfully.")
