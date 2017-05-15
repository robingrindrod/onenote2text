#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, sys

from requests_oauthlib import OAuth2Session
from oauthlib.oauth2 import MobileApplicationClient
import html2text

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

def create_directories_for_sections(session, directory, **kwargs):
    section_groups = api.get_section_groups(session, **kwargs)
    for section_group in section_groups:
        path = os.path.join(directory, section_group['name'])
        os.mkdir(path)
        create_directories_for_sections(path, section_group_id=section_group['id'])

    sections = api.get_sections(session, **kwargs)
    for section in sections:
        path = os.path.join(directory, section['name'])
        os.mkdir(path)
        create_files_for_pages(session, path, section_id=section['id'])

def create_files_for_pages(session, directory, section_id):
    pages = api.get_pages(session, section_id)
    for page in pages:
        content = api.get_page_content(session, page['id'])
        text = html2text.html2text(content)
        path = os.path.join(directory, page['title'] + '.md')
        with open(path, 'w') as file:
            file.write(text)

directory = sys.argv[1]
session = get_authenticated_session()
notebooks = api.get_notebooks(session)
notebook = get_notebook_from_user(notebooks)
create_directories_for_sections(session, directory, notebook_id=notebook['id'])
