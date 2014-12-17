from links import normalize_links
from urlparse import urlparse

def replace_forms(soup, request):
	proxy_url_parse = urlparse(request.build_absolute_uri())
	for form in soup.findAll('form', {'action':True}):
		form['action'] = proxy_url_parse.scheme + '://' + proxy_url_parse.netloc + '/viewpage/'+normalize_links(form['action'], request)
	return soup		

def replace_iframes(soup, request):
	proxy_url_parse = urlparse(request.build_absolute_uri())
	for iframe in soup.findAll('iframe', {'src':True}):
		iframe['src'] = proxy_url_parse.scheme + '://' + proxy_url_parse.netloc + '/viewpage/'+normalize_links(iframe['src'], request)
	return soup