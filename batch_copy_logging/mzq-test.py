import shutil
import os
from datetime import datetime
import concurrent.futures
import json

# Define source and destination paths
source_dir = r"E:\001-MZQ Compliance Services\_Wrapper\Generated Wraps"
dest_dir = r"E:\MZQPlans-test"
foldr="D:/logs"

# Define log file path and state file path
log_file = foldr + r"/copy.log"
state_file =  foldr + r"/copy_state.json"

def log_message(title, message):
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    full_message = f"[{timestamp}] {title}: {message}"
    with open(log_file, "a") as f:
        f.write(full_message + "\n")
    print(full_message)

def load_state():
    if os.path.exists(state_file):
        with open(state_file, "r") as f:
            return json.load(f)
    return {}

def save_state(state):
    with open(state_file, "w") as f:
        json.dump(state, f)

def copy_file(src, dest, state):
    if os.path.isdir(src):
        shutil.copytree(src, dest, dirs_exist_ok=True)
    else:
        os.makedirs(os.path.dirname(dest), exist_ok=True)
        shutil.copy2(src, dest)
    state[src] = True
    save_state(state)

def copy_files_in_batches(src, dest, batch_size=5):
    if not os.path.exists(dest):
        os.makedirs(dest)

    state = load_state()
    all_items = [os.path.join(src, item) for item in os.listdir(src)]
    remaining_items = [item for item in all_items if item not in state]

    batches = [remaining_items[i:i + batch_size] for i in range(0, len(remaining_items), batch_size)]
    
    for batch_number, batch in enumerate(batches, start=1):
        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = {executor.submit(copy_file, item, os.path.join(dest, os.path.relpath(item, src)), state): item for item in batch}
            for future in concurrent.futures.as_completed(futures):
                try:
                    future.result()
                except Exception as e:
                    log_message("ERROR", f"Error copying {futures[future]}: {e}")
        log_message("INFO", f"Batch {batch_number} copied: {len(batch)} items")

# Record start time
start_time = datetime.now()
log_message("INFO", f"Copy started at: {start_time}")

# Perform the copy operation in batches
copy_files_in_batches(source_dir, dest_dir, batch_size=5)

# Record end time
end_time = datetime.now()
log_message("INFO", f"Copy completed at: {end_time}")

# Calculate and log time elapsed
time_elapsed = end_time - start_time
log_message("INFO", f"Time elapsed: {time_elapsed}")

print(f"Copy completed. Check the log file at {log_file} for details.")
