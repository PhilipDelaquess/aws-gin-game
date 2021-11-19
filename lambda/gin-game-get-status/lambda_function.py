import json
import dynamo

def lambda_handler (event, context):
    playerId = event['pathParameters']['id']
    table = dynamo.get_table()
    player = dynamo.get_item(table, playerId)
    return {
        "isBase64Encoded": False,
        "statusCode": 200,
        'headers': {
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
        },
        "body": json.dumps(player)
    }
