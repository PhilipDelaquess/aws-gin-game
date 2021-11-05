import boto3
import decimal

def getTable ():
    return boto3.resource('dynamodb').Table('philip-delaquess-gin-game')

def _replaceDecimals (obj):
    if isinstance(obj, list):
        for i in range(len(obj)):
            obj[i] = _replaceDecimals(obj[i])
        return obj
    elif isinstance(obj, dict):
        for k in obj.keys():
            obj[k] = _replaceDecimals(obj[k])
        return obj
    elif isinstance(obj, decimal.Decimal):
        if obj % 1 == 0:
            return int(obj)
        else:
            return float(obj)
    else:
        return obj

def getItem (table, id, failIfMissing=True):
    response = table.get_item(Key={'id': id}, ConsistentRead=True)
    if failIfMissing or 'Item' in response:
        # might throw KeyError
        return _replaceDecimals(response['Item'])
    else:
        return None

def putItem (table, item):
    table.put_item(Item=item)
