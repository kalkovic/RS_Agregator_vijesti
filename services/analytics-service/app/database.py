import boto3
from botocore.exceptions import ClientError
import os

dynamodb = boto3.resource(
    'dynamodb',
    endpoint_url=os.getenv('DYNAMODB_URL', 'http://dynamodb-local:8000'),
    region_name=os.getenv('AWS_DEFAULT_REGION', 'eu-central-1'),
    aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID', 'test'),
    aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY', 'test')
)

TABLE_NAME = "news-events" 
table = dynamodb.Table(TABLE_NAME)

def get_all_news_events():
    try:
        response = table.scan()
        data = response.get('Items', [])
        
        while 'LastEvaluatedKey' in response:
            response = table.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
            data.extend(response.get('Items', []))
            
        return data
    except ClientError as e:
        print(f"Greška pri čitanju baze: {e.response['Error']['Message']}")
        return []