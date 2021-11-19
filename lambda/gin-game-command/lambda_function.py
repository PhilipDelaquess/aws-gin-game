import json
import impl

def lambda_handler(event, context):
    command = json.loads(event['body'])
    playerId = command['id']
    action = command['action']
    card = command['abbrev'] if 'abbrev' in command else None

    player = impl.performCommand(playerId, action, card)

    return {
        'statusCode': 200,
        'headers': {
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
        },
        'body': json.dumps(player)
    }
