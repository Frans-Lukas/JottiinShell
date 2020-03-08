import argparse
import configparser
import json
import os
import getpass
import sys
from datetime import datetime
from dateutil import parser

import requests


def ask_for_password():
    if sys.stdin.isatty():
        password = getpass.getpass(prompt="Password: ")
    else:
        password = sys.stdin.readline().rstrip
    return password


def change_or_create_credential_store():
    config = configparser.ConfigParser()
    config[CREDENTIALS_KEY] = {}
    config[CREDENTIALS_KEY][USERNAME_KEY] = ask_for_username()
    config[CREDENTIALS_KEY][PASSWORD_KEY] = ask_for_password()
    with open(CREDENTIAL_STORE_PATH, 'w') as configfile:
        config.write(configfile)
    print('Credentials stored in ' + CREDENTIAL_STORE_PATH)


def ask_for_username():
    if sys.stdin.isatty():
        username = input("Email: ")
    else:
        username = sys.stdin.readline().rstrip()
    return username


def config_store_exists():
    if os.path.isfile(CREDENTIAL_STORE_PATH):
        config = configparser.ConfigParser()
        config.read(CREDENTIAL_STORE_PATH)
        if CREDENTIALS_KEY in config \
                and USERNAME_KEY in config[CREDENTIALS_KEY] \
                and PASSWORD_KEY in config[CREDENTIALS_KEY]:
            return True
    return False


def retrieve_credentials_from_store():
    config = configparser.ConfigParser()
    config.read(CREDENTIAL_STORE_PATH)
    return config[CREDENTIALS_KEY][USERNAME_KEY], config[CREDENTIALS_KEY][PASSWORD_KEY]


def authenticate():
    if config_store_exists():
        return retrieve_credentials_from_store()
    print("No credential store found. Save your credentials by using the --auth flag.")
    user = ask_for_username()
    passw = ask_for_password()
    return user, passw


PASSWORD_KEY = 'password'
USERNAME_KEY = 'username'
CREDENTIALS_KEY = 'credentials'
API = 'https://jotti.in/api'
TEST_API = 'http://localhost:8000/api'
AP_JOTTS = '/jotts/'
EMPTY_ARGUMENT = 'no_jott'
CREDENTIAL_STORE_PATH = 'jotti_credential_store.ini'

argparser = argparse.ArgumentParser(description='Take notes')
g = argparser.add_mutually_exclusive_group()
g.add_argument('--jott', '--take-note', type=str, help='Stores the given note.', default=EMPTY_ARGUMENT)
g.add_argument('--auth', '--login', dest='auth', action='store_true', default=False,
               help='stores jotti.in credentials for future use.')
g.add_argument('--notes', '--view-notes', '--jotts', dest='view_notes', action='store_true', default=False,
               help='Shows the latest notes.')

args = argparser.parse_args()

if args.auth:
    change_or_create_credential_store()


def post_note(username, password, text):
    response = requests.post(TEST_API + AP_JOTTS, data={'note_text': text}, auth=(username, password))
    print(response.text)


if not args.jott == EMPTY_ARGUMENT:
    username, password = authenticate()
    post_note(username, password, args.jott)


def get_jotts(username, password):
    next_url = TEST_API + AP_JOTTS
    while next_url is not None:
        response = requests.get(next_url, auth=(username, password))
        parsed_json = response.json()
        if 'detail' in parsed_json:
            print(parsed_json['detail'])
            break
        else:
            next_url = parsed_json['next']
            results = parsed_json['results']
            for result in results:
                date = parser.parse(result['pub_date']).strftime('%Y-%m-%d %H:%M:%S')
                print(str(date) + ": " + result['note_text'])


if args.view_notes:
    username, password = authenticate()
    get_jotts(username, password)
