import json

from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow

from .aws_sdk import BotoWrapper


def google_credentials(scopes):
    # The CLIENT_SECRETS_FILE variable specifies the name of a file that contains
    # the OAuth 2.0 information for this application, including its client_id and
    # client_secret. You can acquire an OAuth 2.0 client ID and client secret from
    # the Google API Console at
    # https://console.developers.google.com/.
    # Please ensure that you have enabled the YouTube Data API for your project.
    # For more information about using OAuth2 to access the YouTube Data API, see:
    #   https://developers.google.com/youtube/v3/guides/authentication
    # For more information about the client_secrets.json file format, see:
    #   https://developers.google.com/api-client-library/python/guide/aaa_client_secrets
    aws_api = BotoWrapper('jongwony-private')
    credential_path = 'google/.credentials'
    credentials = aws_api.deserialize(credential_path)

    # If there are no (valid) credentials available, let the user log in.
    if not credentials or not credentials.valid:
        if credentials and credentials.expired and credentials.refresh_token:
            credentials.refresh(Request())
        else:
            with open('client_secrets.json') as f:
                config = json.load(f)
            flow = InstalledAppFlow.from_client_config(config, scopes=scopes, redirect_uri='http://localhost:8080')
            credentials = flow.run_local_server()

        # Save the credentials for the next run
        aws_api.serialize(credential_path, credentials)

    return credentials
