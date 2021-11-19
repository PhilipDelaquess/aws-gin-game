# Troubleshooting API Gateway
import boto3
from pprint import pprint

client = boto3.client('apigateway')

manual_api_id = [x['id'] for x in client.get_rest_apis()['items'] if x['name'] == 'GinGameAPI'][0]
devops_api_id = [x['id'] for x in client.get_rest_apis()['items'] if x['name'] == 'devops-gin-game-api'][0]

manual_rsrc = [x['id'] for x in client.get_resources(restApiId=manual_api_id)['items'] if x['path'] == '/new-player'][0]
devops_rsrc = [x['id'] for x in client.get_resources(restApiId=devops_api_id)['items'] if x['path'] == '/new-player'][0]

print('MANUAL OPTIONS INTEGRATION')
pprint(client.get_integration(restApiId=manual_api_id, resourceId=manual_rsrc, httpMethod='OPTIONS'))

print('DEVOPS OPTIONS INTEGRATION')
pprint(client.get_integration(restApiId=devops_api_id, resourceId=devops_rsrc, httpMethod='OPTIONS'))

print('MANUAL OPTIONS INTEGRATION RESPONSE')
pprint(client.get_integration_response(restApiId=manual_api_id, resourceId=manual_rsrc, httpMethod='OPTIONS', statusCode='200'))

print('DEVOPS OPTIONS INTEGRATION RESPONSE')
pprint(client.get_integration_response(restApiId=devops_api_id, resourceId=devops_rsrc, httpMethod='OPTIONS', statusCode='200'))

print('MANUAL OPTIONS METHOD RESPONSE')
pprint(client.get_method_response(restApiId=manual_api_id, resourceId=manual_rsrc, httpMethod='OPTIONS', statusCode='200'))

print('DEVOPS OPTIONS METHOD RESPONSE')
pprint(client.get_method_response(restApiId=devops_api_id, resourceId=devops_rsrc, httpMethod='OPTIONS', statusCode='200'))

print('MANUAL POST INTEGRATION')
pprint(client.get_integration(restApiId=manual_api_id, resourceId=manual_rsrc, httpMethod='POST'))

print('DEVOPS POST INTEGRATION')
pprint(client.get_integration(restApiId=devops_api_id, resourceId=devops_rsrc, httpMethod='POST'))

