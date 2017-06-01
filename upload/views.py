from django.shortcuts import render
from django.template.context_processors import csrf
from django.views.decorators.csrf import csrf_exempt

from upload.control import FileUploadControl

from apputil import *
## debug
from pprint import pprint

## User file upload
@csrf_exempt
@post_required
@login_required
def fileupload(request):
	pprint(request.POST)
	pprint(request.FILES)

	error = None
	upload = None
	fileupload = FileUploadControl()
	if fileupload.parseRequest(request) and fileupload.validate():
		upload = fileupload.register()
		if upload == None:
			error = fileupload.get_errors()
	else:
		error = fileupload.get_errors()

	#upload = Klass(id = 2)
	if error == None:
		return JsonResponse({'status': 200,
			'message':'successfuly uploaded',
			'data': {'upload_id': upload.id} })
	else:
		return JsonResponse({'status': 401, 'error': error })
