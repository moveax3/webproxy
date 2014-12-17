from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
from urlparse import urlparse

### validate url
def validate_url(url):
	"""Validate url. Input: url string, return true to success validate or false, if string is not url """
	print url
	validator = URLValidator()
	try:
		validator(url)
		return True
	except ValidationError, e:
		return False

## Replase all links on webproxy links in soup html
def replace_links(soup, request):
	proxy_link_parse = urlparse(request.build_absolute_uri())
	for link in soup.findAll('a', {'href':True}):
		link['href'] = proxy_link_parse.scheme+'://'+proxy_link_parse.netloc+'/viewpage/'+normalize_links(link['href'], request)
	return soup

## reduction all links to form : http[s]://domain/path
def normalize_links(href, request):
	href = href.strip()
	parse_href = urlparse(href)
	site_parse_href = urlparse(request.session['referer'])
	if len(parse_href.path) > 0:
		if parse_href.path[0] is not '/':
			target_path = '/'+parse_href.path 
		else:
			target_path = parse_href.path
	else:
	 	target_path = ''

	if parse_href.scheme == '':
		if parse_href.netloc == '':
			return site_parse_href.scheme+'://'+site_parse_href.netloc+target_path # no domain, no scheme
		else:
			return site_parse_href.scheme+'://'+parse_href.netloc+target_path # yes domain, no scheme
	else:
		return href

