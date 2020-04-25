import jmespath
from googleapiclient.discovery import build

from .secrets import google_credentials


def generate_playlist():
    # This OAuth 2.0 access scope allows for read-only access to the authenticated
    # user's account, but not other types of account access.
    youtube = build(
        'youtube',
        'v3',
        credentials=google_credentials(["https://www.googleapis.com/auth/youtube.readonly"]),
    )

    # Retrieve the contentDetails part of the channel resource for the
    # authenticated user's channel.
    channels_response = youtube.channels().list(
        mine=True,
        part="contentDetails"
    ).execute()

    for channel in channels_response["items"]:
        # From the API response, extract the playlist ID that identifies the list
        # of videos uploaded to the authenticated user's channel.
        uploads_list_id = channel["contentDetails"]["relatedPlaylists"]["uploads"]
        print("Videos in list %s" % uploads_list_id)

        # Retrieve the list of videos uploaded to the authenticated user's channel.
        playlist_items_list_request = youtube.playlistItems().list(
            playlistId=uploads_list_id,
            part="snippet",
            maxResults=20
        )

        while playlist_items_list_request:
            playlist_items_list_response = playlist_items_list_request.execute()
            yield from playlist_items_list_response["items"]
            playlist_items_list_request = youtube.playlistItems().list_next(
                playlist_items_list_request,
                playlist_items_list_response,
            )


def youtube_cards():
    def formatter(x):
        return jmespath.search(
            'snippet | {title: title, description: description, id: resourceId.videoId}',
            x,
        )

    return [formatter(item) for item in generate_playlist()]
