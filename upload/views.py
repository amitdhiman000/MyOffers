from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from upload.forms import FileUploadForm
from base.apputil import *


## User file upload
@csrf_exempt
@App_LoginRequired
def fileupload(request):
	print(request.POST, request.FILES)
	ret = None
	form = FileUploadForm()
	if form.parseForm(request) and form.clean() and form.validate():
		ret = form.commit()

	if ret != None:
		return JsonResponse({'status': 200,
			'message':'successfuly uploaded',
			'data': {'upload_id': ret.id} })
	else:
		return JsonResponse({'status': 401, 'error': form.errors() })
