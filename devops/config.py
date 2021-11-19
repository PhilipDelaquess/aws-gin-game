account_number = '353269244577'

role_arn = 'arn:aws:iam::ACC_NUM:role/lambda-apigateway-role'.replace('ACC_NUM', account_number)

_lambda_uri_template = 'arn:aws:apigateway:us-east-2:lambda:path/2015-03-31/functions/arn:aws:lambda:us-east-2:ACC_NUM:function:LAMBDA_FUNCTION/invocations'.replace('ACC_NUM', account_number)

_gateway_arn_template = 'arn:aws:execute-api:us-east-2:ACC_NUM:API_ID/*'.replace('ACC_NUM', account_number)

def make_lambda_arn (lambda_func):
    return _lambda_uri_template.replace('LAMBDA_FUNCTION', lambda_func)

def make_gateway_arn (api_id):
    return _gateway_arn_template.replace('API_ID', api_id)

# This prefix is inserted before the dynamo table name, the s3 bucket name,
# each lambda function name, and the gateway api name.
# Deploying with a different prefix allows multiple simultaneous instances of
# the same cloud app.
prefix = 'devops-'

dynamo = {
    'table_name': 'gin-game',
    'partition_key': 'id'
}

api_gateway = {
    'name': 'gin-game-api',
    'stage': 'prod'
}
