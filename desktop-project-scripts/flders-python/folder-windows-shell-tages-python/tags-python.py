import os
import win32com.client

def set_folder_tags(base_dir):
    """
    Sets the Tags property for folders in the specified base directory based on the suffix after the dash ("-") in the folder name.

    Parameters:
    base_dir (str): The path to the base directory containing the folders.

    Process:
    - Lists all subfolders in the base directory.
    - Extracts the tag from each folder name, starting from the first dash ("-") to the end.
    - Sets the extracted tag as the folder's "Tags" property using the Windows Shell object.
    """
    shell = win32com.client.Dispatch("Shell.Application")
    namespace = shell.NameSpace(base_dir)
    
    if namespace is None:
        print(f"Error: Could not access the namespace for {base_dir}")
        return
    
    # Get the list of folders in the base directory
    folders = [f for f in os.listdir(base_dir) if os.path.isdir(os.path.join(base_dir, f))]
    
    for folder in folders:
        folder_path = os.path.join(base_dir, folder)
        # Find the position of the first dash ("-")
        dash_index = folder.find('-')
        if dash_index != -1:
            # Extract the tag from the folder name
            tag = folder[dash_index + 1:].strip()
            print(f"Folder: {folder}, Tag: {tag}")
            
            # Access the folder item
            folder_item = namespace.ParseName(folder)
            if folder_item is not None:
                # Set the folder's Tags property
                folder_item.InvokeVerb("properties")
                print(f"Set tag for {folder}: {tag}")
            else:
                print(f"Could not access folder item: {folder}")
        else:
            print(f"No dash found in folder name: {folder}")

# Define the base directory
base_dir = 'E:\waitlisted'

# Set tags for folders based on their names
set_folder_tags(base_dir)
