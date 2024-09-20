
import pandas as pd
from openpyxl import load_workbook

def convert_xlsm_to_csv(xlsm_path, output_csv_path):
    workbook = load_workbook(xlsm_path, data_only=True)
    sheet = workbook.active
    data = sheet.values
    columns = next(data)
    df = pd.DataFrame(data, columns=columns)
    df.to_csv(output_csv_path, index=False)
