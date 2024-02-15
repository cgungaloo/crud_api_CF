# CRUD Application with AWS Lambdas Deployed with Cloud Formation


<img src="images/Amazon_Lambda_architecture_logo.svg.png" width=100 height=100//><img src="images/api_gateway_logo.jpeg" width=100 height=100/><img src="images/Python-logo-notext.svg.png" width=100 height=100/><img src="images/boto3.jpeg" width=100 height=100/>
<img src="images/cloudformation_logo.png" width=100 height=100/><img src="images/cloudwatch.png" width=100 height=100/>
<img src="images/sns_logo.png" width=100 height=100/>
<img src="images/aws-s3-logo-1.png" width=100 height=100/>
<img src="images/aws-vpc2188.logowik.com.webp" width=100 height=100/>




## Introduction

As part of my onboarding to a finance client I was required to learn some AWS skills. I have only dabbled with AWS as a hobby and necer used it directly on a project.

To upskill for this role I created a REST API using AWS resources and deployed it into a VPC via Cloud formation.

This post goes into the Technologies I used and the implementation.

Ive tried to implement a solution that automates as much as possible as well as build an API that us unit tested.

## Technologies

For this Project I use
<ul>
<li><a href="https://www.python.org/">Python</a> A general purpose programming language. We will use this to build out the business logic for the lambdas.</li>
<li><a href="https://pypi.org/project/boto3/">boto3</a> A python library that serves as an AWS client. Used to interact with AWS resources. We use this in our lambda functions to Perform CRUD operations against dynamoDB</li>
<li><a href="https://aws.amazon.com/dynamodb/">AWS DynamoDB</a> A NoSQL Serverless DB service managed by AWS and as such requires no installation on your part you just connect to it through boto3 using an IAM role with sufficient permissions.. We use this service as the DB for our CRUD application. </li> 
<li><a href="https://aws.amazon.com/pm/lambda/?gclid=Cj0KCQiA5rGuBhCnARIsAN11vgSwbY2VZZMY59uih7jf0i8xING5E40hRSexnVEdsSTKoGndmdu3xqgaAn_FEALw_wcB&trk=27324d1f-ee08-40b9-8e7b-5ac228e2fecc&sc_channel=ps&ef_id=Cj0KCQiA5rGuBhCnARIsAN11vgSwbY2VZZMY59uih7jf0i8xING5E40hRSexnVEdsSTKoGndmdu3xqgaAn_FEALw_wcB:G:s&s_kwcid=AL!4422!3!651612449951!e!!g!!aws%20lambda!19836376234!148728884764">AWS Lambdas</a> Lambdas are a serverless AWS resource for writng a range of applications. No managing of services or environments. Code will be uploaded via a zip file to AWS. From my side this makes implementation fairly light weight and allows me to focus more in the application development rather than environment management.</li>
<li><a href="https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/Welcome.html">AWS CloudFormation</a> AWS's answer to infrastructure as code. We will be using this to build out the deployment of our application in the form of a version controlled script. This will include the providsioning of the custom VPC, IAM roles, lambdas, API gateway etc. Cloud formation works on the basis of describing resources as yml code (can also be JSON). When Run. AWS will produce a stack of your resources. The stack can be deleted which in turn will delete all the created resurces. It allows the provisioning of resources to be automated as well as groupes.</li>
<li><a href="https://aws.amazon.com/cloudwatch/">AWS CloudWatch</a> A service used for capturing application logs. I created a log group that our lambda functions used. I also set up an example of an alarm to send emails when lambda function fails.</li>
<li><a href="https://aws.amazon.com/api-gateway/">AWS API Gateway</a> The Lambdas will be exposed to the outside world as HTTP REST endpoints. API gatway facilitates this as a managed service. This allows lambdas to be swapped out when needed and it is yet another piece of infrastructure managed by AWS.</li>
<li><a href="https://aws.amazon.com/sns/">AWS Simple Notification Service</a> A managed publish and subscribe service. It is versatile messaging service with a number of use cases. For this project I use for sending Emails when the alarm is triggered (Application to person, A2P).</li>
<li><a href="https://aws.amazon.com/pm/serv-s3/?gclid=Cj0KCQiA5rGuBhCnARIsAN11vgSwaFC9cBWcZBTlBzw0ueCz2wkGmnRBiPyoMG8t9p-VIGmItz2sQHsaAqj1EALw_wcB&trk=777b3ec4-de01-41fb-aa63-cde3d034a89e&sc_channel=ps&ef_id=Cj0KCQiA5rGuBhCnARIsAN11vgSwaFC9cBWcZBTlBzw0ueCz2wkGmnRBiPyoMG8t9p-VIGmItz2sQHsaAqj1EALw_wcB:G:s&s_kwcid=AL!4422!3!638364429349!e!!g!!amazon%20s3%20block%20storage!19096959014!142655567223">Simple Storage Solution - S3</a> An object storage solution managed by AWS. We use this to upload zip files of the lambda functions written in python</li>
<li><a href="https://docs.aws.amazon.com/vpc/latest/userguide/what-is-amazon-vpc.html">Virtual Private Cloud - VPC</a>The AWS account will have a default VPC but this application will demonstrate the creation of a custom VPC with cloudformation. A VPC is a lgoical virtual network inside AWS. Resources inside the VPC will be private to other VPCs in AWS. Subnets are assigned and can be distributed across multiple Availability zones</li>
</ul>

# Implementation

I orginally started out this  project by building it manually withing AWS. Once I got it working I then implemented it cloudformation.
Here I will try to demonstrate the key components side by side.

## Architectural Diagram:

This is  a simplified diagram of the application and how its deployed in AWS.

<img src="images/sysarch.jpg">
<br/>
<br/>

# Lambda Functions

As a full example of one of the functions Ill focus on ***lambdas/create_articles.py***
```python

import json
import boto3
from botocore.exceptions import ClientError
import datetime
import logging
import os

def lambda_handler(event, context):
    logger = logging.getLogger()
    logger.setLevel("INFO")
    
    logger.info(type(event))
    logger.info(event)
    logger.info("Event json %s" % json.dumps(event))
    logger.info("Context %s" % context)

    client = boto3.resource('dynamodb')

    table = client.Table(os.environ['TableName'])

    http_res = {}
    http_res['headers'] = {}
    http_res['headers']['Content-Type'] = 'application/json'

    eventDateTime = (datetime.datetime.now()).strftime("%Y-%m-%d %H:%M:%S")
    published = False
    try:
        response = table.put_item(
                Item = {
                    'id': context.aws_request_id,
                    'title': event['queryStringParameters']['title'],
                    'description': event['queryStringParameters']['description'],
                    'published': published,
                    'createdAt': eventDateTime,
                    'updatedAt': eventDateTime
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
    http_res['body'] = 'Record ' + context.aws_request_id + ' added'
    
    return http_res

```

### Explanation

I start by declaring the function name *"lambda_hander"*. This can be any name but its important as it will be used to in the cloudformation script as a reference
A logger is also intialised and set to INFO so that we can log aspects of the function at runtime.

We then need to intialise an object that represent resources in AWS. In this case, as we are interacting with dyanmoDB, we need an instantiation of dynamoDB. We use boto3 to do this.

```python
    client = boto3.resource('dynamodb')

    table = client.Table(os.environ['TableName'])
```

We then use the instantiation to then instantiat a table inside dynamoDB. The table name is 'articles' this is passed in as an environment variable which I set up on my machine (In Cloudformation we set up this environment variable)

Once established we then use the table.put_item to take the data from the *event* function input. This variable comes from the lambda function and will contain the inputs from the API endpoint.

put_item expects an *Item* input. I populate this using the *queryStringParameters* which comes from *event*. Each value in *Item* will be a field in the articles table.

I also raise some ClientExceptions and KeyError exceptions in the event that boto3 fails or if the input does not contain the the DB fields I expect.

Once the put_item function successfully runs, I then return the response in the form of a dictionary as *http_res*

This function will be used by our API gateway to create articles. Its a function that will be called once the PUT request is made. I personally appreciated the modular approach that AWS lambdas lends itself to. You'll later see how it gets integrated to the API gateway.

As you can see in the repo I repeat this process for other CRUD operations but use different boto3 functions. In *lambdas/get_all_articles.py* for example, I use the scan function to read data.
Each function essentially follows the principle of Intialising AWS resources with boto3, attempting to interact with the dynamoDB table, raising exceptions in the event of a failure, return a http response object as JSON. Check out each of the functions in the lambdas directory.

## Unit Testing

To Ensure the quality of each lambda function I introduced unit testing for both positive and negative cases. The following is an example of a postive test case for get_all_articles

```python
class Test(TestCase):

    def setUp(self):
        os.environ["TableName"] = "articles"
    
    @patch("boto3.resource")
    def test_get_all_articles(self, mock_resource):
        event = {"queryStringParameters": 
                    {"title":"mytitle"}}
        context = "context_test"

        mock_table = Mock()
        mock_table.scan.return_value = {'Items':'responseval'}
        mock_resource.return_value.Table.return_value = mock_table
        response = get_all_lambda(event,context)

        mock_resource.return_value.Table.assert_called_with('articles')
        mock_table.scan.assert_called_with(
            FilterExpression= Attr('title').begins_with("mytitle")
        )

        assert response['statusCode'] == 200
        assert response['headers']['Content-Type'] == 'application/json'
        assert response['body'] == '"responseval"'
```

### Explanation
Because this is unit test we do not want to perform any real interactions with AWS resources. This could cause adverse affects to our infrastructure which would essentially become an E2E test. I therefore mock the boto3.resource to avoid external calls. In this test Im only interested in checking the function works, not dynamoDB.

To set up the mock I create a fake event and populate it with  queryStringParameters. I put a title in the dictionary.

We then mock the Mock.scan function by assigning its return value with a fake response. This is done using the .return_value function from the unittest framework.

The mock is then assigned as a return value to the Table instantiation. This because Table is an object instatiation rather than a function.

With the mock set up we can run our function, *get_all_lambda*. When the function runs any references to Table and scan are replaced with out mock and the fake response is returned.

Once the function has completed we can then run some assertions.
I assert theat the Table instation has been called with 'artcles' (set by the environment variable in setUp) as a parameter.

I also assert the boto3.resource('dynamod').Table('articles').scan function was called with the filter expression 'title'. The input for the filter expression came from the fake event specified in the test.

I also assert the status code, headers and the body of the HTTP response dictionary.

