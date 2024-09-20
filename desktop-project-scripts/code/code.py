import pandas as pd
import os

# Path to the CSV file
csv_path = 'E:/projcode/excel/idOfNames.csv'

# Load the CSV file
data = pd.read_csv(csv_path)

# Directory where the folders will be created
base_dir = 'E:/test/'

# Create the base directory if it doesn't exist
os.makedirs(base_dir, exist_ok=True)

# Create a folder for each code
for index, row in data.iterrows():
    code = row['Code']
    folder_path = os.path.join(base_dir, str(code))
    os.makedirs(folder_path, exist_ok=True)

print(f"Folders created in {base_dir}")
