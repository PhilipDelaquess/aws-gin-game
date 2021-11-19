# AWS Gin Game

Let's redo the Dropwizard game.

The static parts go in an S3 bucket.

But we Ajax to an API Gateway with different URL, hence CORS issues

API Gateway invokes Lambda functions that manipulate a DynamoDB table.

## IAM

lambda-apigateway-role
lambda-apigateway-policy

## S3

### How it looks now that I've built it by hand

one bucket named philip-delaquess-gin-game in US East (Ohio) us-east-2 with Public access
objects
	contains index.html, style.css, and js/
properties
	static website hosting enabled
	hosting type bucket hosting
permissions
	block public access off
	bucket policy allows everybody to get objects
	no CORS configuration (must be api gateway who cares)

### How to deploy it from scratch with a Python boto3 script

## DynamoDB

## Hosting the Web Page

- Copied the web assets folder from my Dropwizard project and named it s3-bucket.
- Created S3 bucket philip-delaquess-gin-game in us-east-2 (Ohio)
- Uploaded index.html, style.css and js/ to the root of the bucket.
- On the Permissions tab, turned off Block Public Access
- Added the Bucket Policy now present there
- On the Properties tab, enabled static hosting and set index.html

My web site is http://philip-delaquess-gin-game.s3-website.us-east-2.amazonaws.com/

On the very first visit, I got the What is your name? and Let's Play Gin! UI.
That is totally awesome. It means that all the require / react mechanism just worked.

When I typed my name and hit Play, I got a 405 method not allowed because I was
trying to POST /api/gin-server/new-player.

Obviously, everything under /api will go to API Gateway.

## Creating a REST API

- Created a REST API named GinGameAPI

post a string to new-player, use boto3 to create a Player#uuid item in philip-delaquess-gin-game

arn:aws:iam::353269244577:role/lambda-apigateway-role

https://41j6orkh98.execute-api.us-east-2.amazonaws.com/prod/

An API method embodies a method request and a method response
method request is a verb plus a resource, with headers, path and query parameters, payload
method response has status code, headers, body

An API Integration also has a request and a response
request involves transforming the data and calling the back-end (eg lambda)
requires IAM role, the ARN of the Lambda function
response is not applicable to proxy integrations

Lambda Proxy integration
	integration's HTTP method is POST
	its URI is the ARN of the lambda
	give API Gateway permission to call lambda

API Gateway passes the entire request object directly to the lambda handler
Access-Control-Allow-Origin: * among the response headers for CORS

CORS
Implement an OPTIONS method that returns
	Access-Control-Allow-Methods
	Access-Control-Allow-Headers
	Access-Control-Allow-Origin
