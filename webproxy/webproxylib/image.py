import urllib2
from links import normalize_links
from urlparse import urlparse

def load_image(url):
	image_socket = urllib2.urlopen(url)
	image_type = image_socket.info().get('Content-Type')
	image_data = image_socket.read()
	return {'content':image_data, 'type':image_type}

def replaced_images_links(soup, request):
	proxy_url_parse = urlparse(request.build_absolute_uri())
	for image in soup.findAll('img',{'src':True}):
		image['src'] = proxy_url_parse.scheme+'://'+proxy_url_parse.netloc+'/viewimage/'+normalize_links(image['src'], request)
	return soup