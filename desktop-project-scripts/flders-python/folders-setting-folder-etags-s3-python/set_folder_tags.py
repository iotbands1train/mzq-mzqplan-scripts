import os
import win32com.client
"""
    Sets the Tags property for folders in the specified directory based on the suffix after the dash ("-") in the folder name.

    Parameters:
    directory (str): The path to the directory containing the folders.

    Process:
    - Iterates through all items in the specified directory.
    - Checks if each item is a directory.
    - If the directory name contains a dash ("-"), extracts the tag from the folder name.
    - Sets the folder's Tags property to the extracted tag using the Windows Shell object.

    Example:
    Given a directory with folders named "project-1", "example-2", and "test":
    - "project-1" will have its Tags property set to "1".
    - "example-2" will have its Tags property set to "2".
    - "test" will not have a tag set as it does not contain a dash.
"""
# Directory containing the folders
directory = 'E:/MZQPlan/waitlisted'

# Initialize the Shell object
shell = win32com.client.Dispatch("Shell.Application")

for folder_name in os.listdir(directory):
    folder_path = os.path.join(directory, folder_name)
    if os.path.isdir(folder_path):
        # Extract the tag from the folder name
        try:
            tag = folder_name.split('-', 1)[1]
            # Access the folder item
            folder_item = shell.Namespace(directory).ParseName(folder_name)
            # Set the folder's Tags property
            folder_item.Properties("System.Keywords").Value = tag
            print(f"Set tag for {folder_name}: {tag}")
        except IndexError:
            print(f"No dash found in folder name: {folder_name}")
