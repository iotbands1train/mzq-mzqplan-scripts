import os
import boto3
import logging
from datetime import datetime
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# Set up logging
log_dir = "C:/s3sync_logs"
if not os.path.exists(log_dir):
    os.makedirs(log_dir)
log_file = os.path.join(log_dir, f"sync_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log")

logging.basicConfig(
    filename=log_file,
    level=logging.INFO,
    format='%(asctime)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

console = logging.StreamHandler()
console.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(message)s', '%Y-%m-%d %H:%M:%S')
console.setFormatter(formatter)
logging.getLogger('').addHandler(console)

# AWS S3 client with optimized configuration
s3 = boto3.client('s3', config=boto3.session.Config(
    max_pool_connections=200,  # Increase the number of simultaneous connections
    retries={'max_attempts': 10}  # Increase the number of retry attempts
))

source1 = "C:/Users/Administrator/Box/001-MZQ Compliance Services/_Wrapper/Generated Wraps"
destination1 = "s3://mzq-mzqplan-s3bucket/mzq-mzqplan-aws-cloud/e_drive/changes"
bucket_name = destination1.split('/')[2]
s3_base_key = '/'.join(destination1.split('/')[3:])

def log_message(message):
    logging.info(message)
    print(message)

def upload_to_s3(local_path):
    relative_path = os.path.relpath(local_path, source1)
    s3_key = os.path.join(s3_base_key, relative_path).replace("\\", "/")
    try:
        s3.upload_file(local_path, bucket_name, s3_key)
        log_message(f"Uploaded {local_path} to s3://{bucket_name}/{s3_key}")
    except Exception as e:
        log_message(f"Error uploading {local_path} to s3://{bucket_name}/{s3_key}: {e}")

class ChangeHandler(FileSystemEventHandler):
    def on_modified(self, event):
        if not event.is_directory:
            log_message(f"File modified: {event.src_path}")
            upload_to_s3(event.src_path)

    def on_created(self, event):
        if not event.is_directory:
            log_message(f"File created: {event.src_path}")
            upload_to_s3(event.src_path)

    def on_moved(self, event):
        if not event.is_directory:
            log_message(f"File moved: {event.src_path}")
            upload_to_s3(event.dest_path)

    def on_deleted(self, event):
        # Handle deletions in S3 if needed
        if not event.is_directory:
            relative_path = os.path.relpath(event.src_path, source1)
            s3_key = os.path.join(s3_base_key, relative_path).replace("\\", "/")
            try:
                s3.delete_object(Bucket=bucket_name, Key=s3_key)
                log_message(f"Deleted s3://{bucket_name}/{s3_key}")
            except Exception as e:
                log_message(f"Error deleting s3://{bucket_name}/{s3_key}: {e}")

if __name__ == "__main__":
    event_handler = ChangeHandler()
    observer = Observer()
    observer.schedule(event_handler, path=source1, recursive=True)
    observer.start()
    log_message(f"Started monitoring {source1} for changes.")

    try:
        while True:
            pass  # Keep the script running
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
