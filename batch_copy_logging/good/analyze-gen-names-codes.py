import os
import shutil
import pandas as pd

# File paths
xlsm_file_path = r'C:\Users\Administrator\Box\001-MZQ Compliance Services\_Wrapper\Wrap Portal Login Generator_3.xlsm'
waitlisted_folder_path = r'E:\waitlisted'
output_folder_path = r'E:\waitlisted-client-name-codes'

# Create the output folder if it doesn't exist
try:
    os.makedirs(output_folder_path, exist_ok=True)
    print(f"Created or verified the existence of the output directory: {output_folder_path}")
except Exception as e:
    print(f"Failed to create output directory: {e}")

# Load the Excel file
try:
    df = pd.read_excel(xlsm_file_path, sheet_name=None)
    sheet_name = list(df.keys())[0]  # Get the first sheet name
    df = pd.read_excel(xlsm_file_path, sheet_name=sheet_name)
    print("Excel file loaded successfully.")
    
    # Print the column names to verify them
    print("Detected columns in the Excel file:", df.columns)
    
except Exception as e:
    print(f"Failed to load Excel file: {e}")
    df = None

if df is not None:
    # Check if required columns exist
    if 'Client Name' not in df.columns or 'Code' not in df.columns:
        print("Required columns 'Client Name' or 'Code' are missing in the Excel file.")
    else:
        # Extract Client Name and Code
        for index, row in df.iterrows():
            client_name = row['Client Name']
            code = row['Code']

            print(f"Processing: Client Name - {client_name}, Code - {code}")

            # Create the folder name
            folder_name = f"{client_name}__{code}"
            new_folder_path = os.path.join(output_folder_path, folder_name)

            # Create the new folder
            try:
                os.makedirs(new_folder_path, exist_ok=True)
                print(f"Created or verified the existence of the folder: {new_folder_path}")
            except Exception as e:
                print(f"Failed to create directory {new_folder_path}: {e}")
                continue

            # Source folder path in E:\waitlisted
            src_folder = os.path.join(waitlisted_folder_path, client_name)

            if os.path.exists(src_folder):
                # Destination folder with the new name
                dest_folder = os.path.join(new_folder_path, f"{code}-{client_name}")

                # Copy the folder
                try:
                    shutil.copytree(src_folder, dest_folder)
                    print(f"Copied {src_folder} to {dest_folder}")
                except Exception as e:
                    print(f"Failed to copy {src_folder} to {dest_folder}: {e}")
            else:
                print(f"Source folder {src_folder} does not exist.")
else:
    print("DataFrame is empty or could not be loaded. Please check the Excel file.")

print("Script completed.")
