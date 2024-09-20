import os
import shutil

"""
    Copies folders from the source base folder to the destination base folder and creates a text file in each copied folder.

    Parameters:
    source_base_folder (str): The path to the source base directory containing the folders to copy.
    dest_base_folder (str): The path to the destination base directory where the folders will be copied.

    Process:
    - Checks if the destination base folder exists; if not, it creates the folder.
    - Iterates through each item in the source base folder.
    - If the item is a folder, it copies the folder to the destination base folder.
    - After copying, it creates a text file in the copied folder with information about the source and destination paths.

    Example:
    Given a source base folder with folders named "example" and "test":
    - "example" will be copied to the destination base folder.
    - "test" will be copied to the destination base folder.
    - A text file named "example.txt" will be created in the "example" folder, containing the copy information.
    - A text file named "test.txt" will be created in the "test" folder, containing the copy information.
"""

# Function to copy folders and create a text file
def copy_folders_and_create_txt(source_base_folder, dest_base_folder):
    # Create the destination base folder if it doesn't exist
    if not os.path.exists(dest_base_folder):
        os.makedirs(dest_base_folder)
        print(f"Created base folder: {dest_base_folder}")

    # Iterate through each folder in the source base folder
    for folder_name in os.listdir(source_base_folder):
        source_folder_path = os.path.join(source_base_folder, folder_name)
        dest_folder_path = os.path.join(dest_base_folder, folder_name)
        
        if os.path.isdir(source_folder_path):
            print(f"Copying folder: {source_folder_path} to {dest_folder_path}")
            shutil.copytree(source_folder_path, dest_folder_path)
            print(f"Copied folder: {source_folder_path} to {dest_folder_path}")
            
            # Create a text file in the new destination folder
            txt_file_path = os.path.join(dest_folder_path, f"{folder_name}.txt")
            with open(txt_file_path, 'w') as txt_file:
                txt_file.write(f"Folder copied from {source_folder_path} to {dest_folder_path}")
            print(f"Created text file: {txt_file_path}")
        else:
            print(f"Skipped non-folder item: {source_folder_path}")

# Define the source and destination base folders
source_base_folder = 'E:/waitlisted'
dest_base_folder = 'E:/waitlisted2'

# Copy folders and create text files
copy_folders_and_create_txt(source_base_folder, dest_base_folder)
