import pandas as pd

def convert_xlsm_to_csv(xlsm_path, csv_path):
    # Read the Excel file and display its sheet names
    excel_data = pd.ExcelFile(xlsm_path, engine='openpyxl')
    print(f"Sheet names: {excel_data.sheet_names}")

    # Assuming we want to read the first sheet, change if necessary
    df = pd.read_excel(xlsm_path, sheet_name=excel_data.sheet_names[0], engine='openpyxl')

    # Debug: Print the content of the Excel file
    print("Excel Data Head:\n", df.head())

    # Convert the data to CSV
    df.to_csv(csv_path, index=False)
    print(f"Converted {xlsm_path} to {csv_path}")

# Define the paths
xlsm_path = 'E:/projcode/excel/Wrap Portal Login Generator_3.xlsm'
csv_path = 'E:/projcode/excel/idOfNames.csv'

# Convert the file
convert_xlsm_to_csv(xlsm_path, csv_path)
