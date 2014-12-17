from links import normalize_links
from httploader import load
from urlparse import urlparse
### Get web page
def get_page(url, request):

	parsed_url = urlparse(url)

	if 'referer' in request.session :
		request.session['referer'] = request.session['referer']
	else :
		request.session['referer'] = request.build_absolute_uri()


	if 'lastsite' in request.session :
		if request.session['lastsite'].find(parsed_url.netloc) == -1 and parsed_url.netloc.find(request.session['lastsite']) == -1:
			request.session['cookies'] = []
			print 'NEW SITE' # debug
			request.session['lastsite'] = parsed_url.netloc
			if 'charset' in request.session:
				request.session['charset'] = False
	else:
		request.session['lastsite'] = parsed_url.netloc


	return load(url, request, True)


def replace_meta(soup, request):
	proxy_url_parse = urlparse(request.build_absolute_uri())
	for meta in soup.findAll('meta',{'http-equiv':'refresh'}):
		print meta
		meta.extract()
	for meta in soup.findAll('meta',{'http-equiv':'Refresh'}):
		meta.extract()
	return soup





