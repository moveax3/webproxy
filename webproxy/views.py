from django.http import HttpResponse
from django.shortcuts import render
from django.http import HttpResponseRedirect

from bs4 import BeautifulSoup

from webproxylib import links
from webproxylib.page import get_page
from webproxylib.page import replace_meta
from webproxylib.style import replase_style_links
from webproxylib.style import load_style
from webproxylib.style import replace_inline_styles
from webproxylib.image import load_image
from webproxylib.image import replaced_images_links
from webproxylib.links import replace_links
from webproxylib.objects import replace_forms
from webproxylib.scripts import replace_scripts
from webproxylib.objects import replace_iframes
from webproxylib.scripts import load_script

import chardet

def page(request):
    if not request.session.exists(request.session.session_key):
        request.session.create() 
    target_url = request.get_full_path()[10:]
    
    disable_javascript = True
    if request.session['javascript_disable'] is True:
        disable_javascript = True
    else:
        disable_javascript = False

    if links.validate_url(target_url) :
        httploader_answer = get_page(target_url, request)
        if httploader_answer['content']:
            request.session['referer'] = target_url ### change refferer
            page = httploader_answer['content']
            
            if 'charset' in request.session:
                if request.session['charset'] is not False:
                    page = page.decode(request.session['charset'], 'ignore')
                else:
                    charset = chardet.detect(page)['encoding']
                    page = page.decode(charset, 'ignore')
                    request.session['charset'] = charset
            else:
                charset = chardet.detect(page)['encoding']
                page = page.decode(charset, 'ignore')
                request.session['charset'] = charset

            soup = BeautifulSoup(page)
            soup = replase_style_links(soup, request) # processing 'link rel=stylesheet' tags
            soup = replaced_images_links(soup, request) # processing 'img' tags
            soup = replace_links(soup, request) # processing 'a' tags
            soup = replace_forms(soup, request) # processing 'form' tags
            soup = replace_scripts(soup, request, disable_javascript) # processing scripts
            soup = replace_meta(soup, request)
            soup = replace_inline_styles(soup, request)
            soup = replace_iframes(soup, request)
            return render(request, 'webproxy/page.html', {'page':soup.prettify(formatter=None)})
        elif httploader_answer['type']:
            if httploader_answer['type'] == 404:
                return HttpResponse('404')
            else:
                return HttpResponse(httploader_answer)
        else:
            return render(request, 'webproxy/incorrect_content_type.html', {'url':target_url})


    else:
        return render(request, 'webproxy/incorrect_url.html', {'url':target_url})


def image(request):
    image_url = request.get_full_path()[11:]
    image = load_image(image_url)
    return HttpResponse(image['content'], image['type'])

def script(request):
    script_url = request.get_full_path()[12:]
    script = load_script(script_url, request)
    return HttpResponse(script['content'], script['type'])

def style(request):
    style_url = request.get_full_path()[11:]
    style = load_style(style_url, request)
    return HttpResponse(style['content'], style['type'])

def index(request):
    if 'webproxy_anonim_javascript' in request.POST:
        request.session['javascript_disable'] = True
    else:
        request.session['javascript_disable'] = False
    if 'url' in request.POST:
        if request.POST['url'][:4] == 'http':
            url = request.POST['url']
        else:
            url = 'http://'+request.POST['url']
        return HttpResponseRedirect('/viewpage/'+url)
    else:
        return render(request, 'webproxy/index.html', {'title':'index page'})

