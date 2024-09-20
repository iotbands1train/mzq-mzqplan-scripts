import os
import csv

# Define the paths
source_folder = "E:\\MZQPlans"
destination_folder = "E:\\test"

def get_folder_names(folder_path):
    """Get a set of folder names in the given directory."""
    return {name for name in os.listdir(folder_path) if os.path.isdir(os.path.join(folder_path, name))}

# Get the folder names from both directories
source_folders = get_folder_names(source_folder)
destination_folders = get_folder_names(destination_folder)

# Determine the missing folders
missing_folders = destination_folders - source_folders
missing_count = len(missing_folders)

# Output the results
print(f"Number of folders missing: {missing_count}")
print("List of missing folders:")
if missing_count > 10:
    with open('missing_folders.csv', 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(["Missing Folders"])
        for folder in missing_folders:
            csv_writer.writerow([folder])
    print("List is too long, saved as 'missing_folders.csv'.")
else:
    for folder in missing_folders:
        print(folder)
