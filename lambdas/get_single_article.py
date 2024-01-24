import json
import boto3
from botocore.exceptions import ClientError
import logging
import os

def lambda_handler(event, context):
    logger = logging.getLogger()
    logger.setLevel("INFO")
    
    client = boto3.resource('dynamodb')
    table = client.Table(os.environ['TableName'])

    http_res = {}
    http_res['headers'] = {}
    http_res['headers']['Content-Type'] = 'application/json'
    
    try:
        response = table.get_item(
            Key={
            'id': event['queryStringParameters']['id']
        }
        )
        
        if 'Item' in response:
            
            http_res['statusCode'] = 200
            http_res['body'] = json.dumps(response['Item'])
            
            return http_res
        else:
            
            http_res['statusCode'] = 400
            http_res['body'] = json.dumps(f'Not item {event['queryStringParameters']['id']}')
            
            return http_res
        
    except ClientError as ce:
        logger.info(f'Got ClientError: {str(ce)}')
        logger.info(f'Exception : {str(ce)}')
        logger.info(f'Returning 500 error')
        http_res['statusCode'] = 500
        http_res['body'] = json.dumps(f'Got ClientError: {str(ce)}')
        return http_res
    except KeyError as ke:
        logger.info(f'Exception : {str(ke)}')
        logger.info(f'Returning 400 error')
        http_res['statusCode'] = 400
        http_res['body'] = json.dumps(f'Got Key Error: {str(ke)}')
        return http_res