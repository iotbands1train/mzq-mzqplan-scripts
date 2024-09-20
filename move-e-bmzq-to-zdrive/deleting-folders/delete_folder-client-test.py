import os
import tqdm

def delete_file(file_path):
    """Delete a single file."""
    try:
        os.remove(file_path)
        print(f"Deleted file: {file_path}")
    except PermissionError:
        print(f"Skipping {file_path} due to permission issues.")
    except Exception as e:
        print(f"Error deleting file {file_path}: {e}")

def delete_directory(dir_path):
    """Delete a single directory."""
    try:
        os.rmdir(dir_path)
        print(f"Deleted directory: {dir_path}")
    except PermissionError:
        print(f"Skipping {dir_path} due to permission issues.")
    except Exception as e:
        print(f"Error deleting directory {dir_path}: {e}")

def force_delete_folder(folder_path):
    """Force delete the specified folder and its contents."""
    try:
        os.system(f'rmdir /S /Q "{folder_path}"')
        print(f"Forcefully deleted: {folder_path}")
    except Exception as e:
        print(f"Error forcefully deleting {folder_path}: {e}")

def main():
    folder_path = r"E:\clients-test"
    
    # Try to delete normally first
    try:
        total_files = sum([len(files) for r, d, files in os.walk(folder_path)])
        with tqdm.tqdm(total=total_files, desc="Deleting files", unit="file") as pbar:
            for root, dirs, files in os.walk(folder_path, topdown=False):
                for name in files:
                    file_path = os.path.join(root, name)
                    delete_file(file_path)
                    pbar.update(1)
                
                for name in dirs:
                    dir_path = os.path.join(root, name)
                    delete_directory(dir_path)
        
        # Finally, remove the top-level folder itself
        delete_directory(folder_path)
        print(f"Successfully deleted: {folder_path}")
    
    except PermissionError:
        print(f"Skipping {folder_path} due to permission issues.")
        print("Attempting force deletion...")
        force_delete_folder(folder_path)

if __name__ == "__main__":
    main()
