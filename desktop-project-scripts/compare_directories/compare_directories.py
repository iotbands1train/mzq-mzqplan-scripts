import os

def get_renamed_folder_names(source_folders):
    """
    Renames folders by taking the part of the original folder name after the dash ("-").

    Parameters:
    source_folders (set): Set of folder names from the source directory.

    Returns:
    Set of renamed folder names.
    """
    renamed_folders = {f.split('-', 1)[1].strip() if '-' in f else f for f in source_folders}
    return renamed_folders

def find_missing_folders(source_dir, destination_dir):
    """
    Finds folders that are present in the source directory but not in the destination directory
    after renaming the source folders to use the part of the original folder name after the dash ("-").

    Parameters:
    source_dir (str): The path to the source directory.
    destination_dir (str): The path to the destination directory.

    Returns:
    List of missing folders with their renamed counterparts.
    """
    # Get the list of folders in the source directory
    source_folders = {f for f in os.listdir(source_dir) if os.path.isdir(os.path.join(source_dir, f))}
    
    # Get the list of folders in the destination directory
    destination_folders = {f for f in os.listdir(destination_dir) if os.path.isdir(os.path.join(destination_dir, f))}
    
    # Generate the set of renamed folders for comparison
    renamed_folders = get_renamed_folder_names(source_folders)
    
    # Find folders that are in the renamed source set but not in the destination directory
    missing_folders = renamed_folders - destination_folders
    
    return missing_folders

# Define the source and destination directories
source_dir = 'E:/waitlisted'
destination_dir = 'E:/waitlisted3'

# Find missing folders
missing_folders = find_missing_folders(source_dir, destination_dir)

print("Folders present in source but not in destination after renaming:")
for folder in missing_folders:
    print(folder)

# Print the missing folders
print(f"Total source folders: {len(os.listdir(source_dir))}")
print(f"Total destination folders: {len(os.listdir(destination_dir))}")
print(f"Total missing folders: {len(missing_folders)}")