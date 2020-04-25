import json
import pickle

import boto3


class BotoWrapper:
    def __init__(self, bucket='jongwony'):
        self.BUCKET = bucket
        self.s3 = boto3.client('s3')
        self.ssm = boto3.client('ssm')

    def access_token(self):
        return self.ssm.get_parameter(Name='/api_key/instagram/fingerstyle')['Parameter']['Value']

    def get_s3(self, key):
        return self.s3.get_object(Bucket=self.BUCKET, Key=key)

    def put_s3(self, key, o):
        self.s3.put_object(Bucket=self.BUCKET, Key=key, Body=o)

    def deserialize(self, key):
        response = self.get_s3(key)
        return pickle.loads(response['Body'].read())

    def serialize(self, key, o):
        self.put_s3(key, pickle.dumps(o))

    def json_serialize(self, key, o):
        self.put_s3(key, json.dumps(o))

    def json_deserialize(self, key):
        response = self.get_s3(key)
        return json.loads(response['Body'].read())
