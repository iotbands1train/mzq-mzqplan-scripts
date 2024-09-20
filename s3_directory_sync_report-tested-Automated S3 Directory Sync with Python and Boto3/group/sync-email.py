import os
import time
import boto3
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from botocore.exceptions import ClientError

# Configurations
monitor_directory = r"E:\001-MZQ Compliance Services\_Wrapper\Generated Wraps"
s3_bucket = "mzq-mzqplan-s3bucket"
s3_base_path = "mzqplan-aws-cloud/c_drive/Box/test"
email_recipient = "mzqplan-3-qa@mzqplan.awsapps.com"
email_sender = "mzqplan-3-qa@mzqplan.awsapps.com"  # Use the SES verified email here
aws_region = "us-west-2"

# Initialize S3 and SES clients
s3_client = boto3.client('s3', region_name=aws_region)
ses_client = boto3.client('ses', region_name=aws_region)

class MonitorHandler(FileSystemEventHandler):
    def on_created(self, event):
        if not event.is_directory:
            self.process_event(event.src_path, 'created')

    def on_modified(self, event):
        if not event.is_directory:
            self.process_event(event.src_path, 'modified')

    def process_event(self, file_path, event_type):
        print(f"{event_type.capitalize()} detected: {file_path}")
        relative_path = os.path.relpath(file_path, monitor_directory)
        s3_path = os.path.join(s3_base_path, relative_path).replace("\\", "/")
        
        # Upload the file to S3
        try:
            s3_client.upload_file(file_path, s3_bucket, s3_path)
            print(f"Uploaded {file_path} to s3://{s3_bucket}/{s3_path}")
            self.send_email_alert(file_path, event_type)
        except ClientError as e:
            print(f"Failed to upload {file_path} to S3: {e}")

    def send_email_alert(self, file_path, event_type):
        subject = f"File {event_type.capitalize()}: {os.path.basename(file_path)}"
        body = f"A file has been {event_type} in the monitored directory.\n\n" \
               f"File: {file_path}\n" \
               f"Uploaded to: s3://{s3_bucket}/{s3_base_path}\n"
        
        try:
            response = ses_client.send_email(
                Source=email_sender,
                Destination={'ToAddresses': [email_recipient]},
                Message={
                    'Subject': {'Data': subject},
                    'Body': {'Text': {'Data': body}}
                }
            )
            print("Email sent! Message ID:", response['MessageId'])
        except ClientError as e:
            print("Error sending email:", e.response['Error']['Message'])

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
