import configparser
import logging
import os
import csv
from s3_utils import download_file, upload_file_to_s3
from converter import convert_xlsm_to_csv

# Configure logging
log_path = r'D:\logs\proj_main_scripts_run_main_ps1'

# Check if the directory exists, if not, create it
if not os.path.exists(log_path):
    os.makedirs(log_path)

logging.basicConfig(
    filename=os.path.join(log_path, 'script_log.txt'),
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

# Load configuration from properties file
config = configparser.ConfigParser()
config.read(r'D:\proj_main\settings\config.properties')

# Print out the configuration to debug
logging.info("Config sections: %s", config.sections())
logging.info("Config defaults: %s", config.defaults())

# Define variables from the properties file
try:
    bucket_name = config['DEFAULT']['bucket_name']
    file_key = config['DEFAULT']['file_key']
    local_file_path = config['DEFAULT']['local_file_path']
    output_csv_path = config['DEFAULT']['output_csv_path']
    csv_file_key = config['DEFAULT']['csv_file_key']
except KeyError as e:
    logging.error(f"Missing configuration key: {e}")
    raise

def create_sample_csv(file_path):
    """Creates a sample CSV file to ensure the output path is functional."""
    logging.info(f"Creating a sample CSV file at {file_path}.")
    data = [
        ['Name', 'Age', 'City'],
        ['Alice', '30', 'New York'],
        ['Bob', '25', 'San Francisco'],
        ['Charlie', '35', 'Chicago']
    ]

    try:
        with open(file_path, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(data)
        logging.info(f"Sample CSV created at {file_path}.")
    except Exception as e:
        logging.error(f"Failed to create sample CSV: {e}")
        raise

def main():
    logging.info("Starting main function.")
    try:
        logging.info('Downloading file and converting to CSV...')
        download_file(bucket_name, file_key, local_file_path)
        convert_xlsm_to_csv(local_file_path, output_csv_path)
        upload_file_to_s3(output_csv_path, bucket_name, csv_file_key)
        logging.info(f'Successfully converted and uploaded {output_csv_path} to s3://{bucket_name}/{csv_file_key}')
    except Exception as e:
        logging.error(f"An error occurred: {e}")

if __name__ == '__main__':
    logging.info("Script execution started.")
    main()
    logging.info("Script execution completed.")
