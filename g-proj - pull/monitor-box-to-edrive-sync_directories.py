import os
import shutil
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# Configurations
monitor_directory = r"C:\Users\Administrator\Box\001-MZQ Compliance Services\_Wrapper\Generated Wraps"
destination_directory = r"E:\test"

class SyncHandler(FileSystemEventHandler):
    def on_any_event(self, event):
        if event.is_directory:
            return  # Skip directory events here, we'll handle them separately

        if event.event_type in ['created', 'modified', 'moved']:
            self.sync_file(event.src_path)

    def sync_file(self, src_path):
        # Compute the destination path
        relative_path = os.path.relpath(src_path, monitor_directory)
        dest_path = os.path.join(destination_directory, relative_path)

        try:
            # Ensure the destination directory exists
            os.makedirs(os.path.dirname(dest_path), exist_ok=True)

            if os.path.isfile(src_path):
                # Copy the file to the destination
                shutil.copy2(src_path, dest_path)
                print(f"Copied {src_path} to {dest_path}")
            elif os.path.isdir(src_path):
                # Create the directory at the destination
                os.makedirs(dest_path, exist_ok=True)
                print(f"Created directory {dest_path}")
        except Exception as e:
            print(f"Failed to sync {src_path}: {e}")

    def on_deleted(self, event):
        # Handle deleted files or directories
        if event.is_directory:
            return

        relative_path = os.path.relpath(event.src_path, monitor_directory)
        dest_path = os.path.join(destination_directory, relative_path)

        try:
            if os.path.isfile(dest_path):
                os.remove(dest_path)
                print(f"Deleted file {dest_path}")
            elif os.path.isdir(dest_path):
                shutil.rmtree(dest_path)
                print(f"Deleted directory {dest_path}")
        except Exception as e:
            print(f"Failed to delete {dest_path}: {e}")

if __name__ == "__main__":
    event_handler = SyncHandler()
    observer = Observer()
    observer.schedule(event_handler, monitor_directory, recursive=True)
    observer.start()
    print(f"Monitoring {monitor_directory} and syncing to {destination_directory}...")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
