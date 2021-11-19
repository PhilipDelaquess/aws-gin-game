import boto3

import config

dynamodb = boto3.resource('dynamodb')

table_name = config.prefix + config.dynamo['table_name']

existingTable = dynamodb.Table(table_name)
print('Deleting existing table, if any...')
try:
    existingTable.delete()
    existingTable.meta.client.get_waiter('table_not_exists').wait(TableName=table_name)
    print('Existing table deleted')
except:
    print('Existing table not deleted')

print('Creating new table...')
newTable = dynamodb.create_table(
    TableName=table_name,
    KeySchema=[
        {
            'AttributeName': config.dynamo['partition_key'],
            'KeyType': 'HASH'
        }
    ],
    AttributeDefinitions=[
        {
            'AttributeName': config.dynamo['partition_key'],
            'AttributeType': 'S'
        }
    ],
    ProvisionedThroughput={
        'ReadCapacityUnits': 5,
        'WriteCapacityUnits': 5
    }
)

newTable.meta.client.get_waiter('table_exists').wait(TableName=table_name)
print('Table created')
