import os
import json
from authlib.integrations.requests_client import AssertionSession
from oauth2client.service_account import ServiceAccountCredentials


def get_credentials():
    home = os.path.expanduser("~")
    cred_file = "weight-loss-track-2020-fbc41f7c95b2.json"
    with open(f"{home}/keys/google/{cred_file}", "r") as f:
        credentials = json.load(f)
    return credentials


def create_assertion_session(scopes):
    credentials = get_credentials()
    token_endpoint = credentials['token_uri']
    issuer = credentials['client_email']
    private_key = credentials['private_key']
    key_id = credentials.get('private_key_id')

    return AssertionSession(
        grant_type=AssertionSession.JWT_BEARER_GRANT_TYPE,
        token_endpoint=token_endpoint,
        issuer=issuer,
        audience=token_endpoint,
        claims={'scope': ' '.join(scopes)},
        subject=None,
        key=private_key,
        header={
            "alg": "RS256",
            "kid": key_id
        },
    )


def get_service_account_credentials(scopes):
    home = os.path.expanduser("~")
    cred_file = "weight-loss-track-2020-fbc41f7c95b2.json"
    path_to_cred_file = f"{home}/keys/google/{cred_file}"
    creds = (ServiceAccountCredentials
             .from_json_keyfile_name(path_to_cred_file, scopes))
    return creds
