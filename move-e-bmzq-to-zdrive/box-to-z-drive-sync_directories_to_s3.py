import os
import shutil
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm
import time

# Paths
source_directory = r"C:\Users\Administrator\Box\001-MZQ Compliance Services"
destination_directory = r"Z:\001-MZQ Compliance Services"
# Maximum number of workers (set to the number of CPU cores * 2 for optimal speed)
max_workers = os.cpu_count() * 2
# Function to copy files, skipping if they already exist and haven't been modified
def copy_file(src, dest):
    try:
        if os.path.exists(dest):
            src_mtime = os.path.getmtime(src)
            dest_mtime = os.path.getmtime(dest)
            if src_mtime <= dest_mtime:
                return  # Skip the copy if the source file is older or same as the destination file
        os.makedirs(os.path.dirname(dest), exist_ok=True)  # Create directories if they don't exist
        shutil.copy2(src, dest)  # Copy file with metadata
    except Exception as e:
        print(f"Failed to copy {src} to {dest}: {e}")
# Function to sync directories
def sync_directories(source, destination):
    start_time = time.time()  # Start timing the sync process  
    # Calculate total number of files
    total_files = sum([len(files) for r, d, files in os.walk(source)])   
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = []
        with tqdm(total=total_files, desc="Sync Progress", unit="files", mininterval=1.0) as pbar:
            for root, dirs, files in os.walk(source):
                for file in files:
                    src_file = os.path.join(root, file)
                    relative_path = os.path.relpath(root, source)
                    dest_file = os.path.join(destination, relative_path, file)
                    futures.append(executor.submit(copy_file, src_file, dest_file))                
            for future in as_completed(futures):
                future.result()  # Ensure each future is completed
                pbar.update(1)  # Update progress bar
    print(f"Sync completed in {time.time() - start_time:.2f} seconds.")  # Log the total sync time
# Run the sync
sync_directories(source_directory, destination_directory)
