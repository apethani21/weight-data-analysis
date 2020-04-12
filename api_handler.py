import os
import json
from oauth2client.service_account import ServiceAccountCredentials


def get_credentials():
    home = os.path.expanduser("~")
    cred_file = "weight-loss-track-2020-fbc41f7c95b2.json"
    with open(f"{home}/keys/google/{cred_file}", "r") as f:
        credentials = json.load(f)
    return credentials


def get_service_account_credentials(scopes):
    home = os.path.expanduser("~")
    cred_file = "weight-loss-track-2020-fbc41f7c95b2.json"
    path_to_cred_file = f"{home}/keys/google/{cred_file}"
    creds = (ServiceAccountCredentials
             .from_json_keyfile_name(path_to_cred_file, scopes))
    return creds
