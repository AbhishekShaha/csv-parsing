# ********Task 2 : CSV Parser *******
import boto3

s3 = boto3.client('s3')
dynamodb = boto3.resource('dynamodb','eu-west-1')

def csv_reader(event, context):
    
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = event['Records'][0]['s3']['object']['key']
    
    obj = s3.get_object(Bucket=bucket, Key=key)
    
    rows = obj['Body'].read().split('\n')
    
    table = dynamodb.Table('batch_data')
    
    with table.batch_writer() as batch:
        for row in rows:
            
            batch.put_item(Item={
                
                'FirstName':row.split(',')[0],
                'LastName':row.split(',')[1],
                'Age':row.split(',')[2]
            })