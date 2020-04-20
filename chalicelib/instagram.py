import asyncio

import jmespath
from requests import Session

from .aws_sdk import BotoWrapper


class InstagramAPISession(Session):
    @staticmethod
    def url(path):
        return f'https://graph.instagram.com{path}'

    def __init__(self):
        super().__init__()
        aws_api = BotoWrapper()
        self.params['access_token'] = aws_api.access_token()


class InstagramPublicSession(Session):
    def __init__(self):
        super().__init__()

    def get(self, *args, **kwargs):
        return super().get(f'https://instagram.com/jongwony_/', params={'__a': 1})


def carousel_sync():
    session = InstagramPublicSession()
    images = jmespath.search(
        'graphql.user.edge_owner_to_timeline_media.edges[].node | '
        '[].{"img-src": display_url, caption: edge_media_to_caption.edges[0].node.text}',
        session.get().json()
    )
    return [image for image in images if '#guitar' in image['caption']]


async def get_media():
    session = InstagramAPISession()
    resp = session.get(session.url('/me/media'))
    recent = 0
    for data in resp.json()['data']:
        media_id = data['id']
        session.params['fields'] = 'id,caption,media_type,media_url,thumbnail_url,timestamp'
        media = session.get(session.url(f'/{media_id}'))
        exports = media.json()
        if '#guitar' in exports['caption']:
            yield exports
            await asyncio.sleep(0)
            recent += 1
        if recent > 5:
            break


async def carousel():
    def formatter(src):
        data = {
            'caption': src['caption'],
        }
        if src['media_type'] == 'VIDEO':
            data['img-src'] = src['thumbnail_url']
        else:
            data['img-src'] = src['media_url']
        return data

    return [formatter(media) async for media in get_media()]


def gallery():
    # return asyncio.run(carousel())
    return carousel_sync()


if __name__ == '__main__':
    print(gallery())
