#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import requests
from requests_oauthlib import OAuth2Session
from oauthlib.oauth2 import MobileApplicationClient

API_ROOT_URL = 'https://www.onenote.com/api/v1.0/me/notes'

# OAuth data
CLIENT_ID = '54278304-2b46-485f-9997-7bf3f89e7ca0'
AUTHORIZATION_BASE_URL = 'https://login.live.com/oauth20_authorize.srf'
REDIRECT_URI = 'https://login.live.com/oauth20_desktop.srf'
SCOPE = ['wl.signin', 'office.onenote']

session = OAuth2Session(client=MobileApplicationClient(client_id=CLIENT_ID),
        client_id=CLIENT_ID, redirect_uri=REDIRECT_URI, scope=SCOPE)
authorization_url = session.authorization_url(AUTHORIZATION_BASE_URL)[0]

print('Visit this address in your browser:')
print(authorization_url)
response = raw_input('Paste the URL you were redicted to here:')
token = session.token_from_fragment(response)

params = {'select': 'id,name'}
notebooks_response = session.get(API_ROOT_URL + '/notebooks', params=params)
notebooks = json.loads(notebooks_response.text)['value']
for num, notebook in enumerate(notebooks, start=1):
    print(str(num) + '. ' + notebook['name'])

notebook_num = int(raw_input('Enter the number of the notebook to convert:'))
notebook = notebooks[notebook_num - 1]
sections_response = session.get(API_ROOT_URL + '/notebooks/' + notebook['id'] + '/sections', params=params)
sections = json.loads(sections_response.text)['value']
for section in sections:
    print(section['name'])
