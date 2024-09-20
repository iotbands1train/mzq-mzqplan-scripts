import os
import time
import smtplib
import shutil
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# Configurations
source_directory = r"C:\Users\Administrator\Box\001-MZQ Compliance Services\_Wrapper\Generated Wraps"
waiting_directory = r"E:\waiting"
denied_directory = r"E:\denied"
analyst_email = "ksmith.complianceholdings@gmail.com"
gmail_user = "ksmith.complianceholdings@gmail.com"
gmail_password = "lion800tiger$C"

# Ensure target directories exist
os.makedirs(waiting_directory, exist_ok=True)
os.makedirs(denied_directory, exist_ok=True)

class ChangeHandler(FileSystemEventHandler):
    def on_modified(self, event):
        if event.is_directory:
            return
        # Extract the file path
        new_file = event.src_path
        self.notify_analyst(new_file)

    def notify_analyst(self, file_path):
        # Create the email
        msg = MIMEMultipart('alternative')
        msg['From'] = gmail_user
        msg['To'] = analyst_email
        msg['Subject'] = "New Change Detected in Source Directory"

        # HTML content
        html_content = f"""
        <html>
        <body>
            <p>A new change has been detected in the source directory:</p>
            <p><strong>File:</strong> {file_path}</p>
            <p>Do you approve or deny this change?</p>
            <a href="http://localhost:5000/approve?file={file_path}">Approve</a> | 
            <a href="http://localhost:5000/deny?file={file_path}">Deny</a>
        </body>
        </html>
        """
        msg.attach(MIMEText(html_content, 'html'))

        # Send the email using Gmail's SMTP server
        try:
            with smtplib.SMTP('smtp.gmail.com', 587) as server:
                server.starttls()
                server.login(gmail_user, gmail_password)
                server.sendmail(gmail_user, analyst_email, msg.as_string())
                print(f"Email sent to {analyst_email} regarding {file_path}")
        except Exception as e:
            print(f"Failed to send email: {e}")

def start_monitoring():
    event_handler = ChangeHandler()
    observer = Observer()
    observer.schedule(event_handler, path=source_directory, recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

if __name__ == "__main__":
    start_monitoring()
