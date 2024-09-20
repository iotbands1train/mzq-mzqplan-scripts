import os

# Define the search path and the file name
search_path = "E:\\projcode\\excel"
search_file_name = "Wrap Portal Login Generator_3.xlsm"

def search_file_in_directory(search_path, search_file_name):
    """Search for a specific file in the given directory and return the name with a code."""
    file_found = False
    for root, dirs, files in os.walk(search_path):
        if search_file_name in files:
            file_found = True
            file_path = os.path.join(root, search_file_name)
            break
    return file_path if file_found else None

# Search for the file
file_path = search_file_in_directory(search_path, search_file_name)

# Output the result
if file_path:
    print(f"File found: {file_path}")
else:
    print(f"File '{search_file_name}' not found in directory '{search_path}'.")
