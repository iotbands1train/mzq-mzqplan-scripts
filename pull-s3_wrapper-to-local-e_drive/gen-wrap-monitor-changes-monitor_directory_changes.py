import os
import time
import shutil

# Directories to monitor and sync
source_directory = r"E:\test"
destination_directory = r"E:\waiting\clients"

def sync_files():
    # Walk through the source directory
    for root, dirs, files in os.walk(source_directory):
        # Compute the relative path from source_directory
        relative_path = os.path.relpath(root, source_directory)
        dest_dir = os.path.join(destination_directory, relative_path)
        
        # Ensure the destination subdirectory exists
        if not os.path.exists(dest_dir):
            os.makedirs(dest_dir)

        # Loop through all the files in the current directory
        for file_name in files:
            source_file = os.path.join(root, file_name)
            dest_file = os.path.join(dest_dir, file_name)

            # Copy the file if it doesn't exist in the destination or if it has been modified
            if not os.path.exists(dest_file) or os.path.getmtime(source_file) > os.path.getmtime(dest_file):
                shutil.copy2(source_file, dest_file)
                print(f"Copied {source_file} to {dest_file}")

def monitor_directory():
    last_modified_times = {}

    while True:
        changes_detected = False
        for root, dirs, files in os.walk(source_directory):
            for file_name in files:
                source_file = os.path.join(root, file_name)
                last_modified_time = os.path.getmtime(source_file)
                
                # If the file is new or has been modified, update the modification time and set the change flag
                if (source_file not in last_modified_times or last_modified_times[source_file] != last_modified_time):
                    last_modified_times[source_file] = last_modified_time
                    changes_detected = True
        
        if changes_detected:
            print(f"Change detected in '{source_directory}'")
            sync_files()
        
        time.sleep(10)  # Check every 10 seconds

if __name__ == "__main__":
    monitor_directory()
