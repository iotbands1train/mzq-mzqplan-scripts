# Wrap Portal Login Generator Project

## Project Overview

The Wrap Portal Login Generator Project is designed to automate the process of monitoring, downloading, converting, and uploading Excel files (.xlsm) from an S3 bucket to CSV format. The project ensures that the latest version of the file is always processed and uploaded back to the S3 bucket, maintaining data integrity and streamlining workflows.

## Key Features

- **Automated Monitoring**: Checks for new versions of the file in the S3 bucket.
- **Efficient Conversion**: Converts .xlsm files to CSV format using Python.
- **Seamless Integration**: Uploads the converted CSV files back to the S3 bucket.
- **Modular Design**: Divided into separate modules for better maintainability and scalability.

## Project Structure

The project consists of the following files:

- `s3_utils.py`: Contains utility functions for interacting with AWS S3.
- `file_utils.py`: Contains utility functions for file operations.
- `converter.py`: Handles the conversion of .xlsm files to CSV format.
- `main.py`: The main script that orchestrates the monitoring, conversion, and uploading processes.
- `run_main.ps1`: A PowerShell script to run the main Python script.

## Prerequisites

- **Python 3.x**: Ensure Python 3.x is installed on your machine.
- **AWS Credentials**: Configure AWS credentials with the necessary permissions to access the S3 bucket.
- **Required Python Packages**: Install the required Python packages using `pip`.

### Installing Required Packages

#### bash
pip install boto3 pandas openpyxl
