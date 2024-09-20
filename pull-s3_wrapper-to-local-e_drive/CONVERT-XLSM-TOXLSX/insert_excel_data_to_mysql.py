import boto3
import mysql.connector
import json
import pandas as pd

def get_secret(secret_name, region_name):
    # Create a Secrets Manager client
    session = boto3.session.Session()
    client = session.client(service_name='secretsmanager', region_name=region_name)

    try:
        get_secret_value_response = client.get_secret_value(SecretId=secret_name)
    except Exception as e:
        raise e

    # Decrypts secret using the associated KMS key.
    secret = get_secret_value_response['SecretString']
    return json.loads(secret)

def load_excel_data(source_file):
    # Load the Excel file
    xls = pd.ExcelFile(source_file)
    
    # Load specific sheets into dataframes
    web_portal_codes_df = pd.read_excel(xls, 'WebPortalCodes')
    decommissioned_df = pd.read_excel(xls, 'Decommissioned')
    
    return web_portal_codes_df, decommissioned_df

def insert_data_to_mysql(db_connection, cursor, table_name, data):
    # Create an insert statement with placeholders for data
    if table_name == "WebPortalCodes":
        insert_query = """
        INSERT INTO WebPortalCodes (ClientName, Code, LoadedOn)
        VALUES (%s, %s, %s)
        """
    elif table_name == "Decommissioned":
        insert_query = """
        INSERT INTO Decommissioned (ClientName, Code, LoadedOn, DateDecommissioned, DecommissionedBy)
        VALUES (%s, %s, %s, %s, %s)
        """
    
    # Insert data row by row
    for record in data:
        cursor.execute(insert_query, tuple(record.values()))
    db_connection.commit()

def main():
    # Secret Manager details
    secret_name = "rds!cluster-43addac0-3d15-4e21-94a0-86aa4f23bac7"  # Replace with your secret name
    region_name = "us-west-1"  # Replace with your AWS region

    # Get the secret values
    secret = get_secret(secret_name, region_name)
    username = secret["username"]
    password = secret["password"]
    host = "mzqplandb1.cluster-custom-cbtfjxphkahd.us-west-1.rds.amazonaws.com"  # Replace with your endpoint
    database = "MZQ_MZQPLAN_DB_SCHEMA"  # Replace with your database name

    # Database connection
    db_connection = mysql.connector.connect(
        host=host,
        user=username,
        password=password,
        database=database
    )
    cursor = db_connection.cursor()

    # Specify the source file path
    source = r'C:\Users\Administrator\Box\001-MZQ Compliance Services\_Wrapper\Wrap Portal Login Generator_3.XLSM'
    
    # Load the data from the Excel file
    web_portal_codes_df, decommissioned_df = load_excel_data(source)
    
    # Convert the dataframes to dictionaries for easier processing
    web_portal_codes_payload = web_portal_codes_df.to_dict(orient='records')
    decommissioned_payload = decommissioned_df.to_dict(orient='records')
    
    # Insert the data into the MySQL tables
    insert_data_to_mysql(db_connection, cursor, "WebPortalCodes", web_portal_codes_payload)
    insert_data_to_mysql(db_connection, cursor, "Decommissioned", decommissioned_payload)
    
    # Close the connection
    cursor.close()
    db_connection.close()

if __name__ == "__main__":
    main()
