from django.shortcuts import render
from django.template.context_processors import csrf
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone

from upload.controls import FileUploadControl
from base.apputil import *
## debug
from pprint import pprint

## User file upload
@csrf_exempt
@App_PostRequired
@App_LoginRequired
def fileupload(request):
	pprint(request.POST)
	pprint(request.FILES)

	error = None
	upload = None
	fileupload = FileUploadControl()
	if fileupload.parseRequest(request) and fileupload.validate():
		upload = fileupload.register()
		if upload == None:
			error = fileupload.errors()
	else:
		error = fileupload.errors()

	#upload = Klass(id = 2)
	if error == None:
		return JsonResponse({'status': 200,
			'message':'successfuly uploaded',
			'data': {'upload_id': upload.id} })
	else:
		return JsonResponse({'status': 401, 'error': error })
