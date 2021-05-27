import os
import asyncio

import jmespath
from requests import Session

from .aws_sdk import BotoWrapper


class InstagramAPISession(Session):
    @staticmethod
    def url(path):
        return f'https://graph.facebook.com/v10.0{path}'

    def __init__(self):
        super().__init__()
        aws_api = BotoWrapper()
        self.params['access_token'] = aws_api.access_token()


class InstagramPublicSession(Session):
    def __init__(self):
        super().__init__()

    def get(self, *args, **kwargs):
        headers = {
            'authority': 'www.instagram.com',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36 Edg/84.0.522.49',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'sec-fetch-site': 'none',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-user': '?1',
            'sec-fetch-dest': 'document',
            'accept-language': 'ko,en;q=0.9,en-US;q=0.8',
        }
        cookies = {'sessionid': '3872333657%3ArsNi7Wg6jpb689%3A17'}
        params = {'__a': 1}
        return super().get(f'https://instagram.com/jongwony_/', params=params, headers=headers, cookies=cookies)


def carousel_sync():
    filename = 'dump.json'
    if os.path.exists(filename):
        import json
        data = json.load(open('dump.json', 'rb'))
    else:
        session = InstagramPublicSession()
        response = session.get()
        data = response.json()
    images = jmespath.search(
        'graphql.user.edge_owner_to_timeline_media.edges[].node | '
        '[].{"img-src": display_url, caption: edge_media_to_caption.edges[0].node.text}',
        data,
    )
    return [image for image in images if image.get('caption') and '#guitar' in image.get('caption')]


async def get_media():
    session = InstagramAPISession()
    resp = session.get(session.url('/17841404009714041/media'))
    recent = 0
    for data in resp.json()['data']:
        media_id = data['id']
        session.params['fields'] = 'id,caption,media_type,media_url,timestamp'
        media = session.get(session.url(f'/{media_id}'))
        exports = media.json()
        if '#guitar' in exports.get('caption', ''):
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
            data['media_url'] = src['thumbnail_url']
        else:
            data['media_url'] = src['media_url']
        return data

    return [formatter(media) async for media in get_media()]


def gallery():
    return asyncio.run(carousel())
    # return carousel_sync()


if __name__ == '__main__':
    print(gallery())
