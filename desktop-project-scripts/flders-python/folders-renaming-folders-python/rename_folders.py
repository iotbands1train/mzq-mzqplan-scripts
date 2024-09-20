import os
"""
Renames folders within the specified base directory by removing the suffix 
after the first dash ("-") in each folder name.

Parameters:
base_folder (str): The path to the base directory containing the folders to rename.

Process:
- Iterates through all items in the base folder.
- Checks if each item is a directory.
- If the directory name contains a dash ("-"), constructs a new folder name by 
    keeping only the part before the dash and renames the folder.
- Non-directory items and directories without a dash are skipped.

Example:
Given a base folder with directories named "folder-1", "example-2", and "test":
- "folder-1" will be renamed to "folder".
- "example-2" will be renamed to "example".
- "test" will remain unchanged.
"""
# Function to rename folders by removing suffix after "-"
def rename_folders(base_folder):
    # Iterate through each folder in the base folder
    for folder_name in os.listdir(base_folder):
        folder_path = os.path.join(base_folder, folder_name)
        
        if os.path.isdir(folder_path):
            # Find the position of the "-"
            dash_index = folder_name.find("-")
            if dash_index != -1:
                # Create new folder name by removing the suffix after "-"
                new_folder_name = folder_name[:dash_index]
                new_folder_path = os.path.join(base_folder, new_folder_name)
                
                # Rename the folder
                print(f"Renaming folder: {folder_path} to {new_folder_path}")
                os.rename(folder_path, new_folder_path)
                print(f"Renamed folder: {folder_path} to {new_folder_path}")
            else:
                print(f"No dash found in folder name: {folder_name}, skipping rename.")
        else:
            print(f"Skipped non-folder item: {folder_path}")

# Define the base folder
base_folder = 'E:/waitlisted2'

# Rename folders
rename_folders(base_folder)
