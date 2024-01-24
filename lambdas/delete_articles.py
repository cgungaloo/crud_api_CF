import boto3
from botocore.exceptions import ClientError
import logging
import json
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
        response = table.delete_item(
            Key={
            'id': event['queryStringParameters']['id']
            }
        )
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
    
    
    http_res['statusCode'] = response['ResponseMetadata']['HTTPStatusCode']
    http_res['body'] = 'Article ' + event['queryStringParameters']['id']+ ' deleted successfully'
    
    return http_res