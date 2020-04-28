import json
import os
from unittest.mock import MagicMock, patch

from chalicelib import youtube
from chalicelib.youtube import youtube_cards


def test_youtube_cards():
    with open(os.path.join('tests', 'mocks', 'my_youtube_play_list.json')) as f:
        content = json.load(f)

    mock = MagicMock()
    mock.return_value = iter(content)
    with patch.object(youtube, 'generate_playlist', new=mock):
        result = youtube_cards()

    print(result)
    assert result[0]["title"] == "나비보벳따우 인트로"
    assert result[0]["privacy"] == "public"
