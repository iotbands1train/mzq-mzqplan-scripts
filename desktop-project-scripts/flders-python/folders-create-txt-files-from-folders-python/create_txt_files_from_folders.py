import os

def create_txt_files_from_folders(base_dir):
    """
    Creates text files in the base directory, each containing information about a corresponding folder in the base directory.

    Parameters:
    base_dir (str): The path to the base directory containing the folders.

    Process:
    - Lists all folders in the base directory.
    - For each folder, creates a text file named after the folder.
    - Writes the folder name, path, and contents (list of files) to the text file.
    - Prints a success message for each created text file.
    - Prints an error message if an exception occurs.

    Example:
    Given a base directory with folders "example" and "test":
    - A text file named "example.txt" will be created, containing the name, path, and contents of the "example" folder.
    - A text file named "test.txt" will be created, containing the name, path, and contents of the "test" folder.
    """
    try:
        # Get the list of folders in the base directory
        folders = [f for f in os.listdir(base_dir) if os.path.isdir(os.path.join(base_dir, f))]
        
        for folder in folders:
            folder_path = os.path.join(base_dir, folder)
            txt_file_path = os.path.join(base_dir, f"{folder}.txt")
            
            with open(txt_file_path, 'w') as txt_file:
                txt_file.write(f"Folder Name: {folder}\n")
                txt_file.write(f"Path: {folder_path}\n")
                txt_file.write("Contents:\n")
                
                # List contents of the folder
                for root, dirs, files in os.walk(folder_path):
                    for file in files:
                        txt_file.write(f"{os.path.join(root, file)}\n")
            
            print(f"Created file: {txt_file_path}")
    
    except Exception as e:
        print(f"An error occurred: {e}")

# Define the base directory   create_txt_files_from_folders.py
base_dir = 'E:/test/'

# Create text files based on folder names
create_txt_files_from_folders(base_dir)
