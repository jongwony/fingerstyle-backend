import json

import boto3


class BotoWrapper:
    BUCKET = 'jongwony'

    s3 = boto3.client('s3')
    ssm = boto3.client('ssm')

    def access_token(self):
        return self.ssm.get_parameter(Name='/api_key/instagram/fingerstyle')['Parameter']['Value']

    def get_s3(self, key):
        return self.s3.get_object(Bucket=self.BUCKET, Key=key)

    def put_s3(self, key, o):
        self.s3.put_object(Bucket=self.BUCKET, Key=key, Body=json.dumps(o))
