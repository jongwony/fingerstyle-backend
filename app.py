import json

from chalice import Chalice, CORSConfig

from chalicelib.aws_sdk import BotoWrapper
from chalicelib.instagram import gallery

cors_config = CORSConfig(
    allow_origin='https://fingerstyle.jongwony.com',
    max_age=3600,
)
app = Chalice(app_name='fingerstyle')
aws_api = BotoWrapper()
cache_key = 'fingerstyle/instagram/jongwony.json'


@app.route('/', cors=cors_config)
def index():
    response = aws_api.get_s3(cache_key)
    return json.load(response['Body'])


@app.schedule('rate(1 day)')
def per_day():
    aws_api.put_s3(cache_key, gallery())
