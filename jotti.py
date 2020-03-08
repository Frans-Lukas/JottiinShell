import argparse
import configparser
import os
import getpass
import sys


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

NO_JOTT = 'no_jott'

CREDENTIAL_STORE_PATH = 'jotti_credential_store.ini'

parser = argparse.ArgumentParser(description='Take notes')
g = parser.add_mutually_exclusive_group()
g.add_argument('--jott', '--take-note', type=str, help='Stores the given note.', default=NO_JOTT)
g.add_argument('--auth', '--login', dest='auth', action='store_true', default=False,
               help='stores jotti.in credentials for future use.')
g.add_argument('--notes', '--view-notes', '--jotts', dest='view_notes', action='store_true', default=False,
               help='Shows the latest notes.')

args = parser.parse_args()

if args.auth:
    change_or_create_credential_store()

if not args.jott == NO_JOTT:
    username, password = authenticate()

if args.view_notes:
    print('view notes')
