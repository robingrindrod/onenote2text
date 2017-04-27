#!/usr/bin/env python
# -*- coding: utf-8 -*-

from requests_oauthlib import OAuth2Session
from oauthlib.oauth2 import MobileApplicationClient

import onenote_api as api

# OAuth data
CLIENT_ID = '54278304-2b46-485f-9997-7bf3f89e7ca0'
AUTHORIZATION_BASE_URL = 'https://login.live.com/oauth20_authorize.srf'
REDIRECT_URI = 'https://login.live.com/oauth20_desktop.srf'
SCOPE = ['wl.signin', 'office.onenote']

def get_token_from_user(authorization_url, session):
    print('Visit this address in your browser:')
    print(authorization_url)
    response = raw_input('Paste the URL you were redicted to here:')
    session.token_from_fragment(response)

def get_notebook_from_user(notebooks):
    for num, notebook in enumerate(notebooks, start=1):
        print(str(num) + '. ' + notebook['name'])
    notebook_num = int(raw_input('Enter the number of the notebook to convert:'))
    return notebooks[notebook_num - 1]

def get_authenticated_session():
    session = OAuth2Session(client=MobileApplicationClient(client_id=CLIENT_ID),
            client_id=CLIENT_ID, redirect_uri=REDIRECT_URI, scope=SCOPE)
    authorization_url = session.authorization_url(AUTHORIZATION_BASE_URL)[0]
    get_token_from_user(authorization_url, session)
    return session


session = get_authenticated_session()
notebooks = api.get_notebooks(session)
notebook = get_notebook_from_user(notebooks)
sections = api.get_sections(session, notebook['id'])
for section in sections:
    print(section['name'])
