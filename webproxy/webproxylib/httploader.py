#from cookielib import CookieJar
#import urllib2
from urlparse import urlparse
from StringIO import StringIO
import gzip
import os.path
from links import normalize_links
#import urllib
import requests
import json
import re
import pickle
import os
import chardet

def load(url, django_request, is_page=False):

    parsed_url = urlparse(url)
    headers = {
    'Accept' : django_request.META['HTTP_ACCEPT'],
    'Accept-Encoding' : django_request.META['HTTP_ACCEPT_ENCODING'],
    'Accept-Language' : django_request.META['HTTP_ACCEPT_LANGUAGE'],
    'Authorization' : '',
    'Host' : parsed_url.netloc,
    'Referer' : django_request.session['referer'],
    'User-Agent' : django_request.META['HTTP_USER_AGENT'],
    'Request-URI' : parsed_url.path,
    }

    cookies = False
    cookies = load_cookies(django_request.session.session_key)
    if cookies is not False:
        print requests.utils.dict_from_cookiejar(cookies)
    requests.max_redirects = 999
    if(len(django_request.POST) > 0):
        post = django_request.POST
        if cookies == False:
            response = requests.post(url, data=post, headers=headers, verify=False, allow_redirects=False)
        else: 
            response = requests.post(url, data=post, headers=headers, cookies=cookies, verify=False, allow_redirects=False)
    else:
        if cookies == False:
            response = requests.get(url, headers=headers, verify=False, allow_redirects=False)
        else:
            response = requests.get(url, headers=headers, cookies=cookies, verify=False, allow_redirects=False)
    
    if response.status_code == requests.codes.ok:
        save_cookie(response.cookies, django_request.session.session_key)
        return {'content':response.content, 'type':response.headers['Content-Type']}
    elif response.status_code == 302 or response.status_code == 301:
        return load(response.headers['location'], django_request, is_page)
    else:
        print response.content
        print response.status_code
        print response.headers
        return {'content':False, 'type':response.status_code}
        
def load_cookies(user_session_key):
    filename = os.path.dirname(os.path.realpath(__file__))+'/cookie'+user_session_key
    if os.path.isfile(filename):
        with open(filename, 'rb') as cookie_file:
            return pickle.load(cookie_file)
    else: return False

def save_cookie(cookie_jar, user_session_key):
    filename = os.path.dirname(os.path.realpath(__file__))+'/cookie'+user_session_key
    old_cookie_jar = load_cookies(user_session_key)
    if old_cookie_jar == False:
        old_cookie_jar = cookie_jar
    else:
        new_cookie_dict = requests.utils.dict_from_cookiejar(cookie_jar)
        old_cookie_jar = requests.utils.add_dict_to_cookiejar(old_cookie_jar, new_cookie_dict)
    with open(filename, 'wb+') as cookie_file:
        pickle.dump(old_cookie_jar, cookie_file)


