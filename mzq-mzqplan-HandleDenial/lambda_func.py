import boto3

def lambda_handler(event, context):
    # Extract parameters from the request
    s3_key = event['queryStringParameters']['s3_key']
    bucket_name = event['queryStringParameters']['bucket_name']
    
    # Perform the denial logic
    # For example, move the file to a "denied" folder in the same bucket
    s3 = boto3.client('s3')
    copy_source = {'Bucket': bucket_name, 'Key': s3_key}
    
    denied_key = f"denied/{s3_key.split('/')[-1]}"
    
    try:
        s3.copy_object(CopySource=copy_source, Bucket=bucket_name, Key=denied_key)
        return {
            'statusCode': 200,
            'body': f"File {s3_key} has been denied and moved to {denied_key}."
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': f"Error: {str(e)}"
        }
