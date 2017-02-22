import re

def get_device(request):

	device = {}

	ua = request.META.get('HTTP_USER_AGENT', '').lower()

	print(ua)
	
	if ua.find("iphone") > 0:
		device['mobile'] = "iphone" + re.search("iphone os (\d)", ua).groups(0)[0]
		
	if ua.find("ipad") > 0:
		device['tablet'] = "ipad"
		
	if ua.find("android") > 0:
		device['mobile'] = "android" + re.search("android (\d\.\d)", ua).groups(0)[0]
		#.translate(None, '.')
		
	if ua.find("blackberry") > 0:
		device['mobile'] = "blackberry"
		
	if ua.find("windows phone os 7") > 0:
		device['mobile'] = "winphone7"
		
	if ua.find("iemobile") > 0:
		device['mobile'] = "winmo"
		
	if len(device) == 0:			# either desktop, or something we don't care about.
		device['desktop'] = "desktop"
	
	# spits out device names for CSS targeting, to be applied to <html> or <body>.
	#device['classes'] = " ".join(v for (k,v) in device.items())
	
	return device


def get_template(request, file_name):
	device = get_device(request)
	if 'mobile' in device:
		print('mobile : '+device['mobile'])
		return 'mobile/'+file_name
	else:
		print('desktop : '+device['desktop'])
		return 'desktop/'+file_name