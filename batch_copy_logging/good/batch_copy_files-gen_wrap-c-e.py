import shutil
import os
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed

# Define source and destination paths
source_dir = r"C:\Users\Administrator\Box\001-MZQ Compliance Services\_Wrapper\Generated Wraps"
dest_dir = r"E:\001-MZQ Compliance Services\_Wrapper\Generated Wraps"
log_file_directory = r'D:/logs/gen-waitlisted'
log_file = os.path.join(log_file_directory, 'copy.log')

# Ensure the log directory exists
if not os.path.exists(log_file_directory):
    os.makedirs(log_file_directory)

def log_message(message):
    with open(log_file, "a") as f:
        f.write(message + "\n")

def copy_item(src, dest):
    try:
        if os.path.isdir(src):
            shutil.copytree(src, dest, dirs_exist_ok=True)
        else:
            if not os.path.exists(os.path.dirname(dest)):
                os.makedirs(os.path.dirname(dest))
            shutil.copy2(src, dest)
        print(f"Copied: {src}")
    except Exception as e:
        print(f"Error copying {src}: {e}")
        log_message(f"Error copying {src}: {e}")

def copy_files_in_parallel(src, dest, max_workers=60):
    if not os.path.exists(dest):
        os.makedirs(dest)

    all_items = [os.path.join(src, item) for item in os.listdir(src)]
    total_items = len(all_items)
    
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {executor.submit(copy_item, item, os.path.join(dest, os.path.relpath(item, src))): item for item in all_items}
        
        for i, future in enumerate(as_completed(futures), start=1):
            item = futures[future]
            try:
                future.result()
                log_message(f"Copied {item}")
                print(f"Progress: {i}/{total_items} files copied")
            except Exception as e:
                log_message(f"Error copying {item}: {e}")
                print(f"Error copying {item}: {e}")

# Record start time
start_time = datetime.now()
log_message(f"Copy started at: {start_time}")
print(f"Copy started at: {start_time}")

# Perform the copy operation in parallel with real-time updates
copy_files_in_parallel(source_dir, dest_dir, max_workers=8)

# Record end time
end_time = datetime.now()
log_message(f"Copy completed at: {end_time}")
print(f"Copy completed at: {end_time}")

# Calculate and log time elapsed
time_elapsed = end_time - start_time
log_message(f"Time elapsed: {time_elapsed}")
print(f"Time elapsed: {time_elapsed}")

print(f"Copy completed. Check the log file at {log_file} for details.")
log_message(f"Copy completed. Check the log file at {log_file} for details.")
