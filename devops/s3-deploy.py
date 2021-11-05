# Create an S3 bucket that will serve a static web site.
# Upload our s3-bucket directory to the new S3 bucket.

import boto3
import os

s3 = boto3.client('s3')

bucket_name = 'philip-delaquess-gin-game'

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
            s3.upload_file(filename, bucket_name, key, ExtraArgs=extra_args)
        elif entry.is_dir():
            upload_objects(prefix + entry.name + '/', path + '/' + entry.name)

upload_objects('', '../s3-bucket')
