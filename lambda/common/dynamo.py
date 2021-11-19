import boto3
import decimal

def get_table ():
    return boto3.resource('dynamodb').Table('_DYNAMO_TABLE_')

def _replace_decimals (obj):
    if isinstance(obj, list):
        for i in range(len(obj)):
            obj[i] = _replace_decimals(obj[i])
        return obj
    elif isinstance(obj, dict):
        for k in obj.keys():
            obj[k] = _replace_decimals(obj[k])
        return obj
    elif isinstance(obj, decimal.Decimal):
        if obj % 1 == 0:
            return int(obj)
        else:
            return float(obj)
    else:
        return obj

def get_item (table, id, failIfMissing=True):
    response = table.get_item(Key={'id': id}, ConsistentRead=True)
    if failIfMissing or 'Item' in response:
        # might throw KeyError
        return _replace_decimals(response['Item'])
    else:
        return None

def put_item (table, item):
    table.put_item(Item=item)
