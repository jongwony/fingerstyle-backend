import boto3
from moto import mock_s3

from chalicelib.aws_sdk import BotoWrapper


@mock_s3
def test_gallery_json_serialize():
    conn = boto3.resource('s3')
    conn.create_bucket(Bucket='jongwony')

    aws_api = BotoWrapper()
    aws_api.json_serialize('test', [{'caption': '1월 1일 #guitar 에 새 생명 불어넣는 중'}])
    result = aws_api.json_deserialize('test')
    print(result)

    assert result[0]['caption'] == '1월 1일 #guitar 에 새 생명 불어넣는 중'


@mock_s3
def test_pickle_serialize():
    conn = boto3.resource('s3')
    conn.create_bucket(Bucket='jongwony')

    aws_api = BotoWrapper()
    aws_api.serialize('test', [1, 2, 3])
    result = aws_api.deserialize('test')
    assert result[0] == 1
