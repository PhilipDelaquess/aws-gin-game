# Create an S3 bucket that will serve a static web site.
# Upload our s3-bucket directory to the new S3 bucket.

import boto3
import os

import config

s3 = boto3.client('s3')

bucket_name = config.prefix + 'philip-delaquess-gin-game'

s3.create_bucket(
    Bucket=bucket_name,
    CreateBucketConfiguration={
        'LocationConstraint': 'us-east-2'
    }
)
waiter = s3.get_waiter('bucket_exists')
waiter.wait(Bucket=bucket_name)

s3.put_bucket_website(
    Bucket=bucket_name,
    WebsiteConfiguration={
        'IndexDocument': {
            'Suffix': 'index.html'
        }
    }
)

s3.put_public_access_block(
    Bucket=bucket_name,
    PublicAccessBlockConfiguration={
        'BlockPublicAcls': False,
        'IgnorePublicAcls': False,
        'BlockPublicPolicy': False,
        'RestrictPublicBuckets': False
    }
)

policy = '''{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "PublicReadGetObject",
            "Effect": "Allow",
            "Principal": "*",
            "Action": "s3:GetObject",
            "Resource": "arn:aws:s3:::BUCKET/*"
        }
    ]
}'''.replace('BUCKET', bucket_name)

s3.put_bucket_policy(
    Bucket=bucket_name,
    Policy=policy
)

api_client = boto3.client('apigateway')
api_name = config.prefix + config.api_gateway['name']
api_id = [x['id'] for x in api_client.get_rest_apis()['items'] if x['name'] == api_name][0]
print('Will inject api ID = ' + api_id)

def upload_objects (prefix, path):
    "Recursive function to traverse a directory tree and upload files to S3"
    for entry in os.scandir(path):
        if not entry.name.startswith('.') and entry.is_file():
            filename = path + '/' + entry.name
            key = prefix + entry.name
            print(key)
            extra_args = {}
            if entry.name.endswith('.html'):
                # otherwise AWS serves it as an attachment which your browser downloads
                extra_args['ContentType'] = 'text/html'
            elif entry.name.endswith('.css'):
                # otherwise the stylesheet doesn't work
                extra_args['ContentType'] = 'text/css'
            if entry.name == 'aws.js':
                js_file = open(filename, 'r')
                js_output = js_file.read()
                js_file.close()
                js_output = js_output.replace('_STAGE_', config.api_gateway['stage'])
                js_output = js_output.replace('_API_ID_', api_id)

                temp_filename = 'temp_aws.js'
                temp_file = open(temp_filename, 'w')
                temp_file.write(js_output)
                temp_file.close()
                s3.upload_file(temp_filename, bucket_name, key, ExtraArgs=extra_args)
                os.remove(temp_filename)
            else:
                s3.upload_file(filename, bucket_name, key, ExtraArgs=extra_args)
        elif entry.is_dir():
            upload_objects(prefix + entry.name + '/', path + '/' + entry.name)

upload_objects('', '../s3-bucket')
