import os
import time
import boto3
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from datetime import datetime, timedelta

# Configurations
monitor_directory = r"E:\001-MZQ Compliance Services\_Wrapper\Generated Wraps"
s3_bucket = "mzq-mzqplan-s3bucket"
s3_base_path = "mzqplan-aws-cloud/c_drive/Box/test"  # Updated S3 base path
sns_topic_arn = "arn:aws:sns:us-west-1:666669385478:mzq-mzqplan-qa3-monitor_and_sync_to_s3"  # Your provided SNS topic ARN
aws_region = "us-west-1"

# Time threshold to suppress duplicate notifications (e.g., 5 minutes)
suppress_duration = timedelta(minutes=5)
last_notified = {}

# Initialize S3 and SNS clients
s3_client = boto3.client('s3', region_name=aws_region)
sns_client = boto3.client('sns', region_name=aws_region)

class MonitorHandler(FileSystemEventHandler):
    def on_any_event(self, event):
        if not event.is_directory and event.event_type in ['created', 'modified']:
            self.process_event(event.src_path, event.event_type)

    def process_event(self, file_path, event_type):
        current_time = datetime.now()
        if file_path in last_notified:
            if current_time - last_notified[file_path] < suppress_duration:
                print(f"Suppressed duplicate notification for {file_path}")
                return
        last_notified[file_path] = current_time

        print(f"{event_type.capitalize()} detected: {file_path}")
        relative_path = os.path.relpath(file_path, monitor_directory)
        s3_path = os.path.join(s3_base_path, relative_path).replace("\\", "/")
        
        # Upload the file to S3
        try:
            s3_client.upload_file(file_path, s3_bucket, s3_path)
            print(f"Uploaded {file_path} to s3://{s3_bucket}/{s3_path}")
            self.send_sns_notification(file_path, event_type)
        except Exception as e:
            print(f"Failed to upload {file_path} to S3: {e}")

    def send_sns_notification(self, file_path, event_type):
        subject = f"File {event_type.capitalize()}: {os.path.basename(file_path)}"
        message = f"A file has been {event_type} in the monitored directory.\n\n" \
                  f"File: {file_path}\n" \
                  f"Uploaded to: s3://{s3_bucket}/{s3_base_path}\n"
        
        try:
            response = sns_client.publish(
                TopicArn=sns_topic_arn,
                Message=message,
                Subject=subject
            )
            print("SNS notification sent! Message ID:", response['MessageId'])
        except Exception as e:
            print(f"Failed to send SNS notification: {e}")

if __name__ == "__main__":
    event_handler = MonitorHandler()
    observer = Observer()
    observer.schedule(event_handler, monitor_directory, recursive=True)
    observer.start()
    print(f"Monitoring {monitor_directory}...")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
