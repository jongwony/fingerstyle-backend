from chalice import Chalice, CORSConfig, Response

from chalicelib.aws_sdk import BotoWrapper
from chalicelib.youtube import youtube_cards
from chalicelib.instagram import gallery

cors_config = CORSConfig(
    allow_origin='https://fingerstyle.jongwony.com',
    allow_headers=['Cross-Origin-Resource-Policy'],
    max_age=3600,
)
app = Chalice(app_name='fingerstyle')
aws_api = BotoWrapper()
instagram_cache_key = 'fingerstyle/instagram/gallery.json'
youtube_cache_key = 'fingerstyle/youtube/playlist.json'


@app.route('/', cors=cors_config)
def index():
    return {}


@app.route('/instagram', cors=cors_config)
def instagram():
    return Response(
        body=aws_api.json_deserialize(instagram_cache_key),
        headers={'Cross-Origin-Resource-Policy': 'cross-origin'},
    )


@app.route('/youtube', cors=cors_config)
def youtube():
    return Response(
        body=aws_api.json_deserialize(youtube_cache_key),
        headers={'Cross-Origin-Resource-Policy': 'cross-origin'},
    )


@app.schedule('rate(1 day)')
def per_day(event):
    print(event.to_dict())
    batch()


def batch():
    aws_api.json_serialize(instagram_cache_key, gallery())
    aws_api.json_serialize(youtube_cache_key, youtube_cards())


if __name__ == '__main__':
    batch()
