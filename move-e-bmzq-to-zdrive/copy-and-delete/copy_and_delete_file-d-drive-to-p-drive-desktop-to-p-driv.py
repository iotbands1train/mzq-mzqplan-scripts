import os
import shutil
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm

def copy_and_delete_file(src, dst):
    """Copy a single file from src to dst and delete the source file."""
    try:
        shutil.copy2(src, dst)
        os.remove(src)
        print(f"Copied and deleted: {src}")
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

def delete_empty_dirs(source_path):
    """Delete empty directories in the source path."""
    for dirpath, dirnames, filenames in os.walk(source_path, topdown=False):
        try:
            os.rmdir(dirpath)
            print(f"Deleted empty directory: {dirpath}")
        except OSError:
            # Directory is not empty
            pass

def main():
    source_path = r"C:\Users\Administrator\Desktop\projcode"
    destination_path = r"P:\desktop-project-scripts"

    # Create the directory structure in the destination
    create_directory_structure(source_path, destination_path)

    # Get all files to copy
    files = get_all_files(source_path)
    
    # Copy files with progress bar and delete the source
    with ThreadPoolExecutor(max_workers=8) as executor:
        futures = []
        for file in files:
            dest_file = os.path.join(destination_path, os.path.relpath(file, source_path))
            futures.append(executor.submit(copy_and_delete_file, file, dest_file))
        
        # Use tqdm for progress tracking
        for _ in tqdm(as_completed(futures), total=len(futures), desc="Copying files", unit="file"):
            pass

    # Delete empty directories
    delete_empty_dirs(source_path)

    print("File copy and folder deletion completed!")

if __name__ == "__main__":
    main()
