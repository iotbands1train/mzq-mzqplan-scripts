import os
import shutil
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm

def copy_file(src, dst):
    """Copy a single file from src to dst."""
    try:
        shutil.copy2(src, dst)
    except Exception as e:
        print(f"Error copying {src} to {dst}: {e}")

def create_directory_structure(source_path, destination_path):
    """Create directory structure in destination path."""
    for dirpath, dirnames, filenames in os.walk(source_path):
        structure = os.path.join(destination_path, os.path.relpath(dirpath, source_path))
        if not os.path.isdir(structure):
            os.makedirs(structure)

def get_all_files(source_path):
    """Get all files to copy."""
    file_paths = []
    for dirpath, _, filenames in os.walk(source_path):
        for filename in filenames:
            file_paths.append(os.path.join(dirpath, filename))
    return file_paths

def main():
    source_path = r"E:\001-MZQ Compliance Services"
    destination_path = r"Z:\001-MZQ Compliance Services"

    # Create the directory structure in the destination
    create_directory_structure(source_path, destination_path)

    # Get all files to copy
    files = get_all_files(source_path)
    
    # Copy files with progress bar
    with ThreadPoolExecutor(max_workers=8) as executor:
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
