import boto3
import pandas as pd
import xlrd

# AWS S3 Configuration
s3_client = boto3.client('s3', region_name='us-west-1')

# Define bucket name and file paths
bucket_name = 'mzq-mzqplan-s3bucket'
file_key = 'mzqplan-aws-cloud/d_drive/wrapper_codes/Wrap Portal Login Generator_3.xls'  # Ensure the correct key is used
local_file_path = 'Wrap_Portal_Login_Generator_3.xls'

# Download the file from S3
s3_client.download_file(bucket_name, file_key, local_file_path)

# Load the Excel file using xlrd
workbook = xlrd.open_workbook(local_file_path)

# Print sheet names to verify
sheet_names = workbook.sheet_names()
print("Sheet names:", sheet_names)

# Function to convert sheet to DataFrame
def sheet_to_df(workbook, sheet_name):
    sheet = workbook.sheet_by_name(sheet_name)
    data = [sheet.row_values(row) for row in range(sheet.nrows)]
    cols = data[0]
    if len(data) > 1:
        return pd.DataFrame(data[1:], columns=cols)
    else:
        print(f"No data in sheet: {sheet_name}")
        return pd.DataFrame()

# Check each sheet for data
for sheet_name in sheet_names:
    df = sheet_to_df(workbook, sheet_name)
    
    if not df.empty:
        local_csv_path = f'{sheet_name}.csv'
        print(f"Data from sheet {sheet_name}:\n", df.head())
        df.to_csv(local_csv_path, index=False)
        print(f"Sheet {sheet_name} has been converted to {local_csv_path}")

        # Upload the CSV file back to S3
        csv_file_key = f'mzqplan-aws-cloud/d_drive/wrapper_codes/{sheet_name}.csv'
        s3_client.upload_file(local_csv_path, bucket_name, csv_file_key)
        print(f"CSV file {local_csv_path} has been uploaded to S3 at {csv_file_key}")
    else:
        print(f"Sheet {sheet_name} is empty or has no data rows.")

print("Conversion and upload process completed.")
