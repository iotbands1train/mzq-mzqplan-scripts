Set objShell = CreateObject("WScript.Shell")
strCmd = """C:\Program Files\Python39\python.exe"" p:\pull-s3_wrapper-to-local-e_drive\CONVERT-XLSM-TOXLSX\insert_excel_data_to_mysql.py"
objShell.Run strCmd, 0, False
