import os
import subprocess
from datetime import datetime

# Define local path and S3 bucket
localpath = r"E:\001-MZQ Compliance Services\_Wrapper\Generated Wraps"
s3bucket = "s3://mzq-mzqplan-s3bucket/mzqplan-aws-cloud/b_drive/MZQ_Wrapper_box"
# Define log file directory and ensure it exists
log_directory = r"D:\logs\push_sync_waitlisted2_s3"
# Check if the directory exists, if not create it
if not os.path.exists(log_directory):
    os.makedirs(log_directory)
# Define log file path
log_file = os.path.join(log_directory, "sync.log")
def log_message(message):
    with open(log_file, "a") as f:
        f.write(message + "\n")
    print(message)
def sync_batch(batch):
    for item in batch:
        s3_dest = os.path.join(s3bucket, os.path.relpath(item, localpath)).replace("\\", "/")
        command = ["aws", "s3", "sync", item, s3_dest, "--delete"]
        result = subprocess.run(command, capture_output=True, text=True)
        log_message(result.stdout)
        if result.stderr:
            log_message(result.stderr)
def batch_sync(src, batch_size=5):
    all_items = [os.path.join(src, item) for item in os.listdir(src)]
    batches = [all_items[i:i + batch_size] for i in range(0, len(all_items), batch_size)]
    for batch_number, batch in enumerate(batches, start=1):
        sync_batch(batch)
        log_message(f"Batch {batch_number} synced: {len(batch)} items")
# Record start time
start_time = datetime.now()
log_message(f"Sync started at: {start_time}")
# Perform the sync operation in batches
batch_sync(localpath, batch_size=5)
# Record end time
end_time = datetime.now()
log_message(f"Sync completed at: {end_time}")
# Calculate and log time elapsed
time_elapsed = end_time - start_time
log_message(f"Time elapsed: {time_elapsed}")
print(f"Sync completed. Check the log file at {log_file} for details.")
