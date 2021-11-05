import boto3

dynamodb = boto3.resource('dynamodb')

tableName = 'philip-delaquess-gin-game'

existingTable = dynamodb.Table(tableName)
print('Deleting existing table, if any...')
try:
    existingTable.delete()
    existingTable.meta.client.get_waiter('table_not_exists').wait(TableName=tableName)
    print('Existing table deleted')
except:
    print('Existing table not deleted')

print('Creating new table...')
newTable = dynamodb.create_table(
    TableName=tableName,
    KeySchema=[
        {
            'AttributeName': 'id',
            'KeyType': 'HASH'
        }
    ],
    AttributeDefinitions=[
        {
            'AttributeName': 'id',
            'AttributeType': 'S'
        }
    ],
    ProvisionedThroughput={
        'ReadCapacityUnits': 5,
        'WriteCapacityUnits': 5
    }
)

newTable.meta.client.get_waiter('table_exists').wait(TableName=tableName)
print('Table created')
