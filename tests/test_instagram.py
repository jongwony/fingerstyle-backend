import json
import os
from dataclasses import dataclass
from unittest.mock import patch

import requests

from chalicelib.instagram import gallery


@dataclass
class MockResponse:
    response_code: int
    json: dict


def test_gallery():
    with open(os.path.join('tests', 'mocks', 'instagram_a.json')) as f:
        content = json.load(f)

    with patch.object(requests, 'get', new=MockResponse(200, content)):
        result = gallery()

    print(result)
    assert result[0]['caption'] == '1월 1일 #guitar 에 새 생명 불어넣는 중'
