from httploader import load
from links import normalize_links
from urlparse import urlparse
import chardet
import re
import string
## replase all  link in soup html
def replase_style_links(soup, request):
    parsed_proxy_url =  urlparse(request.build_absolute_uri())
    for css_file in soup.findAll('link',{'href':True}):
        css_file['href'] = parsed_proxy_url.scheme+'://'+parsed_proxy_url.netloc+'/viewstyle/'+normalize_links(css_file['href'], request)
        print css_file['href'] # debug
    return soup

## load style file
def load_style(url, request):
    httploader_answer = load(url, request)
    content = replace_instyle_links(httploader_answer['content'], request)
    content_type = httploader_answer['type']
    return {'content':content, 'type':content_type}

## replase links inside style
def replace_instyle_links(style_content, request):
    parsed_proxy_url =  urlparse(request.build_absolute_uri())
    image_proxy_url_part = parsed_proxy_url.scheme+'://'+parsed_proxy_url.netloc+'/viewimage/'
    
    for link in re.findall('url\(([^)]+)\)', style_content):
        link = normalize_links(link.replace('"', '').replace("'", ''), request)
        replaced_link = '"'+image_proxy_url_part+link+'"'
        print image_proxy_url_part  
        if style_content.find(replaced_link) == -1:
            style_content = style_content.replace(link, replaced_link)
    
    return style_content

## processing inlinse styles in soup html
def replace_inline_styles(soup, request):
    for style in soup.findAll('style'):
        if(len(style.contents) >0):
            style.contents[0] = replace_instyle_links(style.contents[0], request)
        print style.contents
    return soup
