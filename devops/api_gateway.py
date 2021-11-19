import boto3
import uuid

import config

client = boto3.client('apigateway')
lambda_client = boto3.client('lambda')

endpoints = [
    {
        'path': 'action',
        'methods': {
            'POST': 'gin-game-command'
        }
    },
    {
        'path': 'new-player',
        'methods': {
            'POST': 'gin-game-new-player'
        }
    },
    {
        'path': '{id}',
        'methods': {
            'GET': 'gin-game-get-status'
        }
    }
]

response = client.create_rest_api(
    name=config.prefix + config.api_gateway['name'],
    endpointConfiguration={
        'types': ['REGIONAL']
    }
)
api_id = response['id']
print('Created API with id ' + api_id)
# NOTE: Will need to inject that id into the 'static' JS Ajax URLs.
# Or discover it with get_rest_apis()

root_resource_id = client.get_resources(restApiId=api_id)['items'][0]['id']

for endpoint in endpoints:
    response = client.create_resource(
        restApiId=api_id,
        parentId=root_resource_id,
        pathPart=endpoint['path']
    )
    resource_id = response['id']

    for (method, lbda) in endpoint['methods'].items():
        client.put_method(
            restApiId=api_id,
            resourceId=resource_id,
            httpMethod=method,
            authorizationType='NONE'
        )
        client.put_method_response(
            restApiId=api_id,
            resourceId=resource_id,
            httpMethod=method,
            statusCode='200',
            responseParameters={
                'method.response.header.Access-Control-Allow-Origin': False
            },
            responseModels={
                'application/json': 'Empty'
            }
        )
        client.put_integration(
            restApiId=api_id,
            resourceId=resource_id,
            httpMethod=method,
            type='AWS_PROXY',
            integrationHttpMethod='POST',
            uri=config.make_lambda_arn(config.prefix + lbda)
        )
        client.put_integration_response(
            restApiId=api_id,
            resourceId=resource_id,
            httpMethod=method,
            statusCode='200',
            responseParameters={
                'method.response.header.Access-Control-Allow-Origin': '\'*\''
            },
            responseTemplates={
                'application/json': ''
            }
        )
        lambda_client.add_permission(
            FunctionName=config.prefix + lbda,
            StatementId=str(uuid.uuid4()),
            Action='lambda:InvokeFunction',
            Principal='apigateway.amazonaws.com',
            SourceArn=config.make_gateway_arn(api_id)
        )

    client.put_method(
        restApiId=api_id,
        resourceId=resource_id,
        httpMethod='OPTIONS',
        authorizationType='NONE'
    )
    client.put_method_response(
        restApiId=api_id,
        resourceId=resource_id,
        httpMethod='OPTIONS',
        statusCode='200',
        responseParameters={
            'method.response.header.Access-Control-Allow-Headers': False,
            'method.response.header.Access-Control-Allow-Origin': False,
            'method.response.header.Access-Control-Allow-Methods': False
        },
        responseModels={
            'application/json': 'Empty'
        }
    )
    client.put_integration(
        restApiId=api_id,
        resourceId=resource_id,
        httpMethod='OPTIONS',
        type='MOCK',
        requestTemplates={
            'application/json': '{"statusCode": 200}'
        }
    )
    client.put_integration_response(
        restApiId=api_id,
        resourceId=resource_id,
        httpMethod='OPTIONS',
        statusCode='200',
        responseParameters={
            'method.response.header.Access-Control-Allow-Headers': "'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token'",
            'method.response.header.Access-Control-Allow-Methods': "'OPTIONS,POST'",
            'method.response.header.Access-Control-Allow-Origin': "'*'"
        },
        responseTemplates={
            'application/json': ''
        }
    )

client.create_deployment(restApiId=api_id, stageName=config.api_gateway['stage'])
