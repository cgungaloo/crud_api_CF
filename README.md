# CRUD Application with AWS Lambdas Deployed with Cloud Formation


<img src="images/Amazon_Lambda_architecture_logo.svg.png" idth=100 height=100//><img src="images/api_gateway_logo.jpeg" width=100 height=100/><img src="images/Python-logo-notext.svg.png" width=100 height=100/><img src="images/boto3.jpeg" width=100 height=100/>
<img src="images/cloudformation_logo.png" width=100 height=100/><img src="images/cloudwatch.png" width=100 height=100/>


## Introduction

As part of my onboarding to a finance client I was required to learn some AWS skills. I have only dabbled with AWS as a hobby and necer used it directly on a project.

To upskill for this role I created a REST API using AWS resources and deployed it into a VPC via Cloud formation.

This post goes into the Technologies I used and the implementation.

Ive tried to implement a solution that automates as much as possible as well as build an API that us unit tested.

## Technologies

For this Project I use

    - Python
        - boto3
    - AWS DynamoDB
    - AWS Lambdas
    - AWS CloudFormation
    - AWS CloudWatch and CloudAlarm
    - AWS API Gateway

# Implementation

I orginally started out this  project by building it manually withing AWS. Once I got it working I then implemented it cloudformation.
Here I will try to demonstrate the key components side by side.




