import json
import impl

def lambda_handler (event, context):
    playerName = event['body']
    player = impl.createNewPlayer(playerName)
    
    return {
        'statusCode': 200,
        'headers': {
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
        },
        'body': json.dumps(player)
    }
