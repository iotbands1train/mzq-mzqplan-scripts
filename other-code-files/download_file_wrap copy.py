import boto3
import pandas as pd

# AWS S3 Configuration
s3_client = boto3.client('s3', region_name='us-west-1')

# Define bucket name and file path
bucket_name = 'mzq-mzqplan-s3bucket'
file_key = 'mzqplan-aws-cloud/d_drive/wrapper_codes/Wrap Portal Login Generator_3.xlsm'  # Ensure the correct key is used
local_file_path = 'Wrap_Portal_Login_Generator_3.xlsm'
output_csv_path = 'Wrap_Portal_Login_Generator_3.csv'

# Download the file from S3
s3_client.download_file(bucket_name, file_key, local_file_path)

# Load the Excel file
xls = pd.ExcelFile(local_file_path)

# Print sheet names to verify
print("Sheet names:", xls.sheet_names)

# Read the first sheet
sheet_name = xls.sheet_names[0]
df = pd.read_excel(xls, sheet_name=sheet_name)

# Print first few rows of the DataFrame to verify data
print("Data preview:\n", df.head())

# Check if the DataFrame is empty
if df.empty:
    print("The DataFrame is empty. Please check the Excel file for data.")
else:
    # Convert to CSV
    df.to_csv(output_csv_path, index=False)
    print(f"File has been converted to {output_csv_path}")
