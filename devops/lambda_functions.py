import boto3
import os
from zipfile import ZipFile

import config

lambda_functions = [
    {
        'name': 'gin-game-command',
        'common': ['card.py', 'dynamo.py']
    },
    {
        'name': 'gin-game-new-player',
        'common': ['card.py', 'dynamo.py']
    },
    {
        'name': 'gin-game-get-status',
        'common': ['dynamo.py']
    }
]

client = boto3.client('lambda')

def get_injected_string (filename):
    text_file = open(filename, 'r')
    contents = text_file.read()
    text_file.close()
    return contents.replace('_DYNAMO_TABLE_', config.prefix + config.dynamo['table_name'])

for lf_desc in lambda_functions:
    name = lf_desc['name']
    src_dir = '../lambda/' + name
    print(config.prefix + name)
    zip_file = ZipFile('temp.zip', 'w')
    for entry in os.scandir(src_dir):
        print('  ' + entry.name)
        zip_file.writestr(entry.name, get_injected_string(src_dir + '/' + entry.name))
    if 'common' in lf_desc:
        for c in lf_desc['common']:
            print('  ' + c)
            zip_file.writestr(c, get_injected_string('../lambda/common/' + c))
    zip_file.close()

    file = open('temp.zip', 'rb')
    bytes_of_zip_data = file.read()
    file.close
    os.remove('temp.zip')

    result = client.create_function(
        FunctionName=config.prefix + name,
        Runtime='python3.8',
        Role=config.role_arn,
        Handler='lambda_function.lambda_handler',
        Code={'ZipFile': bytes_of_zip_data},
        Publish=True,
        PackageType='Zip'
    )
