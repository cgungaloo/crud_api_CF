# CRUD application with AWS

A REST API built with python lambda functions.
The application is deployed using a cloud formation with specific roles for each lambda.
The application writes and reads data from a dynamoDB table.
It also uses has a custom cloud watch group with and expiry.
Unit tests have also been written for the lambda function.
Lambdas are manually Zipped and uploaded to S3 from where the cloudwatch downloads them.


