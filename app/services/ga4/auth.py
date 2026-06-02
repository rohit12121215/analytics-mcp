import os

from dotenv import load_dotenv

from google.oauth2.credentials import Credentials

from google_auth_oauthlib.flow import InstalledAppFlow

from google.auth.transport.requests import Request


load_dotenv()

SCOPES = [
    "https://www.googleapis.com/auth/analytics.readonly"
]

TOKEN_FILE = "token.json"


def get_credentials():

    creds = None

    if os.path.exists(TOKEN_FILE):

        creds = Credentials.from_authorized_user_file(
            TOKEN_FILE,
            SCOPES
        )

    if not creds or not creds.valid:

        if creds and creds.expired and creds.refresh_token:

            creds.refresh(Request())

        else:

            flow = InstalledAppFlow.from_client_secrets_file(
                "credentials.json",
                SCOPES
            )

            creds = flow.run_local_server(port=0)

        with open(TOKEN_FILE, "w") as token:

            token.write(creds.to_json())

    return creds