# Import necessary modules from local files
from config_loader import load_config  # Function to load configuration settings
from file_checker import file_exists   # Function to check if a file exists
from s3_utils import get_s3_client, upload_file_to_s3  # Functions to interact with AWS S3
from logger import setup_logger  # Function to set up logging
import os
# Constants
CONFIG_FILE_PATH = 'D:/proj_main_livegen/upload_to_s3_project/settings/config.properties'  # Path to the configuration file

# Define the log file path
log_dir = r'D:/logs/proj_sync_webgen_s3'
LOG_FILE_PATH = os.path.join(log_dir, 'script_log.txt')

# Ensure the directory exists
if not os.path.exists(log_dir):
    os.makedirs(log_dir)
  

def main():
    """
    Main function that orchestrates the process of loading configurations,
    setting up logging, checking file existence, and uploading the file to S3.
    """
    # Setup logging
    logger = setup_logger(LOG_FILE_PATH)  # Initialize the logger
    logger.info("Starting script execution.")  # Log the start of the script

    # Load configuration
    config = load_config(CONFIG_FILE_PATH)  # Load configurations from the specified file
    region_name = config['region_name']  # Extract AWS region name from config
    local_file_path = config['local_file_path']  # Extract local file path from config
    bucket_name = config['bucket_name']  # Extract S3 bucket name from config
    s3_file_key = config['s3_file_key']  # Extract S3 file key from config

    # Log the loaded configuration
    logger.info(f"Configuration loaded: region_name={region_name}, local_file_path={local_file_path}, bucket_name={bucket_name}, s3_file_key={s3_file_key}")

    # AWS S3 Client
    s3_client = get_s3_client(region_name)  # Get an S3 client using the specified region name

    # Check if file exists
    if file_exists(local_file_path):  # Check if the local file exists
        logger.info(f"File {local_file_path} exists. Starting upload.")  # Log file existence
        result = upload_file_to_s3(s3_client, local_file_path, bucket_name, s3_file_key)  # Upload the file to S3
        logger.info(result)  # Log the result of the upload operation
    else:
        logger.error(f"File {local_file_path} does not exist.")  # Log an error if the file does not exist

    logger.info("Script execution completed.")  # Log the completion of the script

if __name__ == '__main__':
    main()  # Execute the main function if this script is run directly
