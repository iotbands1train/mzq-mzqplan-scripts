import openpyxl
from openpyxl import load_workbook

def convert_xlsm_to_xlsx(input_file, output_file):
    # Load the .xlsm file
    workbook = load_workbook(input_file, keep_vba=False)
    
    # Save it as .xlsx file
    workbook.save(output_file)
    print(f"File converted and saved as {output_file}")

# Example usage
input_file = r'C:\Users\Administrator\Box\001-MZQ Compliance Services\_Wrapper/Wrap Portal Login Generator_3.xlsm'  # Replace with your .xlsm file path
output_file = r'Z:\Wrap Portal Login Generator_3.xlsx'  # Replace with your desired .xlsx output path

convert_xlsm_to_xlsx(input_file, output_file)
