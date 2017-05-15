import json

API_ROOT_URL = 'https://www.onenote.com/api/v1.0/me/notes'

def get_notebooks(session):
    return __get_object(session, API_ROOT_URL + '/notebooks')

# If both notebook_id and section_group_id are specified, the section_group_id
# will be ignored.
def get_section_groups(session, notebook_id=None, section_group_id=None):
    url = API_ROOT_URL
    if notebook_id:
        url += '/notebooks/' + notebook_id
    elif section_id:
        url += '/sectionGroups/' + section_group_id
    url += '/sectionGroups'
    return __get_object(session, url)

# If both notebook_id and section_group_id are specified, the section_group_id
# will be ignored.
def get_sections(session, notebook_id=None, section_group_id=None):
    url = API_ROOT_URL
    if notebook_id:
        url += '/notebooks/' + notebook_id
    elif section_id:
        url += '/sectionGroups/' + section_group_id
    url += '/sections'
    return __get_object(session, url)

def get_pages(session, section_id=None):
    url = API_ROOT_URL
    if section_id:
        url += '/sections/'+ section_id
    url += '/pages'
    return __get_object(session, url)

def get_page_content(session, page_id):
    url = API_ROOT_URL + '/pages/' + page_id + '/content'
    return session.get(url).text

def __get_object(session, url):
    response = session.get(url)
    return json.loads(response.text)['value']
