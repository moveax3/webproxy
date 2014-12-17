from links import normalize_links
from urlparse import urlparse
from httploader import load

def replace_scripts(soup, request, is_disable_scripts):
	if is_disable_scripts is True:
		for js in soup.findAll('script'):
			js.extract()
		return soup
	else:
		parse_proxy_url = urlparse(request.build_absolute_uri())
		for js_file in soup.findAll('script',{'src':True}):
			js_file['src'] = parse_proxy_url.scheme+'://'+parse_proxy_url.netloc+'/viewscript/'+normalize_links(js_file['src'], request)
		return soup


def load_script(url, request):
	httploader_answer = load(url, request)
	content = httploader_answer['content']
	content_type = httploader_answer['type']
	return {'content':content, 'type':content_type}

