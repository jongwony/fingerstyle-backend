from chalice import Chalice, CORSConfig

from chalicelib.instagram import gallery

cors_config = CORSConfig(
    allow_origin='https://fingerstyle.jongwony.com',
    max_age=3600,
)
app = Chalice(app_name='fingerstyle')


@app.route('/', cors=cors_config)
def index():
    return gallery()
