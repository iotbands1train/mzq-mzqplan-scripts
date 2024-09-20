import os
import shutil
import pandas as pd

# File path to the Excel file
xlsm_file_path = r'C:\Users\Administrator\Box\001-MZQ Compliance Services\_Wrapper\Wrap Portal Login Generator_3.xlsm'

# Load the Excel file from the WebPortalCodes sheet
df = pd.read_excel(xlsm_file_path, sheet_name='WebPortalCodes')

# Path to the source and destination directories
waitlisted_folder_path = r'C:\Users\Administrator\Box\001-MZQ Compliance Services\_Wrapper\Generated Wraps'
output_folder_path = r'E:\waitlisted-client-name-codes'

# Extract Client Name and Code, generate folder names, create folders, and copy files
for index, row in df.iterrows():
    client_name = row['Client Name']
    code = str(row['Code'])  # Convert code to string
    folder_name = f"{client_name}-{code}"
    new_folder_path = os.path.join(output_folder_path, folder_name)
    
    # Source folder path in E:\waitlisted
    src_folder = os.path.join(waitlisted_folder_path, code)
    
    # Create the new folder if it doesn't exist
    if not os.path.exists(new_folder_path):
        os.makedirs(new_folder_path)
        print(f"Created folder: {new_folder_path}")
    else:
        print(f"Folder already exists: {new_folder_path}")
    
    # Copy files from the related folder in E:\waitlisted to the new folder
    if os.path.exists(src_folder):
        # Copy the contents of the source folder to the destination folder
        shutil.copytree(src_folder, new_folder_path, dirs_exist_ok=True)
        print(f"Copied files from {src_folder} to {new_folder_path}")
    else:
        print(f"Source folder {src_folder} does not exist.")

print("Script completed.")
