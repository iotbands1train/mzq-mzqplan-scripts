import os
import shutil
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm
import re

def copy_file(src, dst):
    """Copy a single file from src to dst."""
    try:
        shutil.copy2(src, dst)
    except Exception as e:
        print(f"Error copying {src} to {dst}: {e}")

def is_valid_directory(directory_name):
    """Check if the directory name starts with a digit (0-9) or a letter (a-z)."""
    return re.match(r'^[0-9a-zA-Z]', os.path.basename(directory_name)) is not None

def create_directory_structure(source_path, destination_path):
    """Create directory structure in destination path for valid directories."""
    for dirpath, dirnames, filenames in os.walk(source_path):
        # Filter directories to only include those that start with a digit or letter
        dirnames[:] = [d for d in dirnames if is_valid_directory(d)]
        structure = os.path.join(destination_path, os.path.relpath(dirpath, source_path))
        if not os.path.isdir(structure):
            os.makedirs(structure)

def get_all_files(source_path):
    """Get all files to copy from valid directories."""
    file_paths = []
    for dirpath, dirnames, filenames in os.walk(source_path):
        # Filter directories to only include those that start with a digit or letter
        dirnames[:] = [d for d in dirnames if is_valid_directory(d)]
        for filename in filenames:
            file_paths.append(os.path.join(dirpath, filename))
    return file_paths

def main():
    source_path = r"Z:\001-MZQ Compliance Services\_Wrapper\Generated Wraps"
    destination_path = r"E:\test\clients"

    # Create the directory structure in the destination
    create_directory_structure(source_path, destination_path)

    # Get all files to copy
    files = get_all_files(source_path)
    
    # Copy files with progress bar
    with ThreadPoolExecutor(max_workers=150) as executor:
        futures = []
        for file in files:
            dest_file = os.path.join(destination_path, os.path.relpath(file, source_path))
            futures.append(executor.submit(copy_file, file, dest_file))
        
        # Use tqdm for progress tracking
        for _ in tqdm(as_completed(futures), total=len(futures), desc="Copying files", unit="file"):
            pass

    print("File copy completed!")

if __name__ == "__main__":
    main()
