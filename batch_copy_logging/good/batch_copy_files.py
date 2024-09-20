import shutil
import os
from datetime import datetime

# Define source and destination paths
source_dir = r"C:\Users\Administrator\Box\001-MZQ Compliance Services\_Wrapper\Generated Wraps"
dest_dir = r"E:\waitlisted"
log_file_directory = r'D:/logs/gen-waitlisted'
log_file = os.path.join(log_file_directory, 'copy.log')

# Ensure the log directory exists
if not os.path.exists(log_file_directory):
    os.makedirs(log_file_directory)


def log_message(message):
    with open(log_file, "a") as f:
        f.write(message + "\n")

def copy_files_in_batches(src, dest, batch_size=5):
    if not os.path.exists(dest):
        os.makedirs(dest)

    all_items = [os.path.join(src, item) for item in os.listdir(src)]
    batches = [all_items[i:i + batch_size] for i in range(0, len(all_items), batch_size)]
    
    for batch_number, batch in enumerate(batches, start=1):
        for item in batch:
            s = item
            d = os.path.join(dest, os.path.relpath(item, src))
            if os.path.isdir(s):
                shutil.copytree(s, d, dirs_exist_ok=True)
            else:
                if not os.path.exists(os.path.dirname(d)):
                    os.makedirs(os.path.dirname(d))
                shutil.copy2(s, d)
        
        log_message(f"Batch {batch_number} copied: {len(batch)} items")
        print(f"Batch {batch_number} copied: {len(batch)} items")

# Record start time
start_time = datetime.now()
log_message(f"Copy started at: {start_time}")
print(f"Copy started at: {start_time}")

# Perform the copy operation in batches
copy_files_in_batches(source_dir, dest_dir, batch_size=5)

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
