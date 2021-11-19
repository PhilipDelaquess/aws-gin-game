import lambda_functions
import api_gateway
import s3
import dynamo

 devops_api_id = [item['id'] for item in client.get_rest_apis()['items'] if item['name'] == 'devops-gin-game-api'][0]
 devops_rsrc = [item['id'] for item in client.get_resources(restApiId=devops_api_id)['items'] if item['path'] == '/action'][0]