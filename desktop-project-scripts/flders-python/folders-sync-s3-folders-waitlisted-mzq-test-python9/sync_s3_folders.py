import os
import subprocess

def extract_codes_from_folders(base_dir):
    """
    Extracts the "Code" from folder names in the specified base directory.

    Parameters:
    base_dir (str): The path to the base directory containing the folders.

    Returns:
    List of tuples containing folder names and extracted codes.
    """
    # Get the list of folders in the base directory
    folders = [f for f in os.listdir(base_dir) if os.path.isdir(os.path.join(base_dir, f))]
    codes = []
    
    for folder in folders:
        # Find the position of the first dash ("-")
        dash_index = folder.find('-')
        if dash_index != -1:
            # Extract the code from the folder name
            code = folder[dash_index + 1:]
            codes.append((folder, code))
        else:
            print(f"No dash found in folder name: {folder}")
    
    return codes

def sync_selected_folders(selected_codes, local_folder_template, s3_folder_template):
    """
    Synchronizes the selected folders with the corresponding S3 folders.

    Parameters:
    selected_codes (list of str): The list of selected codes for synchronization.
    local_folder_template (str): The template path for the local folder with a placeholder for the code.
    s3_folder_template (str): The template path for the S3 folder with a placeholder for the code.
    """
    for code in selected_codes:
        local_folder = local_folder_template.replace("{Code}", code)
        s3_folder = s3_folder_template.replace("{Code}", code)

        if not os.path.exists(local_folder):
            print(f"Local folder does not exist: {local_folder}")
            continue

        if not os.path.exists(os.path.dirname(s3_folder)):
            os.makedirs(os.path.dirname(s3_folder))
            print(f"Created S3 folder: {os.path.dirname(s3_folder)}")
        
        try:
            # Perform the sync using aws s3 sync command
            command = f'aws s3 sync "{local_folder}" "{s3_folder}"'
            subprocess.run(command, check=True, shell=True)
            print(f"Sync Successful: {local_folder} to {s3_folder}")
        except subprocess.CalledProcessError as e:
            print(f"Sync failed: {e}")

# Define the base directory and folder templates
base_dir = 'E:/waitlisted'
local_folder_template = 'C:/Users/Administrator/Box/001-MZQ Compliance Services/{Code}'
s3_folder_template = 'E:/test/{Code}'

# Check if the local folder template path is valid
if not os.path.exists(os.path.dirname(local_folder_template.replace("{Code}", ""))):
    print(f"Error: The base directory for the local folder template does not exist: {os.path.dirname(local_folder_template.replace('{Code}', ''))}")
    exit(1)

# Extract codes from folder names
codes = extract_codes_from_folders(base_dir)

# Display the list of folders and extracted codes
print("Available folders and codes:")
for idx, (folder, code) in enumerate(codes):
    print(f"{idx + 1}. Folder: {folder}, Code: {code}")

# Get user selection
selected_indices = input("Enter the numbers of the folders you want to sync, separated by commas: ")
selected_indices = [int(i.strip()) - 1 for i in selected_indices.split(',') if i.strip().isdigit()]

# Extract the selected codes
selected_codes = [codes[idx][1] for idx in selected_indices if idx >= 0 and idx < len(codes)]

# Confirm with the user before proceeding
print("Selected Codes for Sync:")
for code in selected_codes:
    print(code)

confirmation = input("Do you want to proceed with the sync operation? (yes/no): ")
if confirmation.lower() == 'yes':
    # Sync the selected folders
    sync_selected_folders(selected_codes, local_folder_template, s3_folder_template)
else:
    print("Sync operation cancelled.")
