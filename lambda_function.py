import json
import boto3
from datetime import datetime

# Initialize S3 client
s3 = boto3.client('s3')

# REPLACE with your actual S3 bucket name
BUCKET_NAME = "demo-s309"

def lambda_handler(event, context):
    print("Received event:", json.dumps(event))
    records = event.get('Records', [])
    
    for record in records:
        body = record['body']
        message_id = record['messageId']
        print(f"Processing message {message_id}: {body}")
        
        # 1. Parse string body to JSON or format as dictionary
        try:
            payload = json.loads(body)
        except json.JSONDecodeError:
            payload = {"raw_content": body}

        # 2. Construct a clean S3 object key (path)
        timestamp = datetime.utcnow().strftime('%Y/%m/%d')
        file_name = f"sqs-data/{timestamp}/{message_id}.json"
        
        # 3. Upload payload to S3
        s3.put_object(
            Bucket=BUCKET_NAME,
            Key=file_name,
            Body=json.dumps(payload, indent=2),
            ContentType='application/json'
        )
        print(f"Successfully uploaded to s3://{BUCKET_NAME}/{file_name}")

    return {
        'statusCode': 200,
        'body': json.dumps('Successfully processed records and saved to S3.')
    }