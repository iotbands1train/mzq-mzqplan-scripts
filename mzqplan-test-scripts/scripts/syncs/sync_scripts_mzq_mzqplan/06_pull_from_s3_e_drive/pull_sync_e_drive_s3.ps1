# Define the S3 bucket and local directory
$s3Bucket = "s3://mzq-mzqplan-s3bucket/mzqplan-aws-cloud/e_drive"
$localDir = "E:\fromS3eDriveTest"

# AWS CLI sync command with exclude parameters
$awsSyncCommand = "aws s3 sync $s3Bucket $localDir --exclude '*/$RECYCLE.BIN/*' --exclude '$.*'"

# Run the command
Invoke-Expression $awsSyncCommand
