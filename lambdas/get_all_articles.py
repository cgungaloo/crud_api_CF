import json
import boto3
import logging
from boto3.dynamodb.conditions import Attr
from botocore.exceptions import ClientError
import os

def lambda_handler(event, context):
    logger = logging.getLogger()
    logger.setLevel("INFO")
    
    logger.info("Event json %s" % json.dumps(event))
    logger.info("Context %s" % context)
    
    http_res = {}
    http_res['headers'] = {}
    http_res['headers']['Content-Type'] = 'application/json'
    
    try:
        client = boto3.resource('dynamodb')
        table = client.Table(os.environ['TableName'])
        
        title = event['queryStringParameters']['title']

        logger.info("Getting Title Filter %s" % title)
    except KeyError as e:
        logger.info(f'Exception : {str(e)}')
        logger.info(f'Returning 400 error')
        http_res['statusCode'] = 400
        http_res['body'] = json.dumps(f'Got Key Error: {str(e)}')
        return http_res
    
    try:
        if not title:
            logger.info("Title is empty")
            response = table.scan()
        else:
            logger.info("Title is not empty")
            
        
        response = table.scan(
                        FilterExpression = Attr('title').begins_with(title)
                        )
    except ClientError as ce:
        logger.info(f'Got ClientError: {str(ce)}')
        logger.info(f'Exception : {str(ce)}')
        logger.info(f'Returning 500 error')
        http_res['statusCode'] = 500
        http_res['body'] = json.dumps(f'Got ClientError: {str(ce)}')
        return http_res
    
    http_res['statusCode'] = 200
    http_res['body'] = json.dumps(response['Items'])
    
    return http_res