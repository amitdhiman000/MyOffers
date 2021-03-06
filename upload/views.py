from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from upload.forms import (FileUploadForm, ImageUploadForm)
from base.apputil import App_LoginRequired


# User file upload
#@App_LoginRequired
def upload_file(request):
    print(request.POST, request.FILES)
    form = FileUploadForm()
    ret = form.process(request)
    if ret:
        return JsonResponse({'status': 200,
            'message': 'successfuly uploaded',
            'data': {'upload_ids': ret.id} })
    else:
        return JsonResponse({'status': 401, 'error': form.errors()})


# User file upload
def upload_image(request):
    print(request.POST, request.FILES)
    form = ImageUploadForm()
    ret = form.process(request)
    if ret:
        return JsonResponse({'status': 200,
                             'message': 'successfuly uploaded',
                             'data': {'upload_ids': ret}})
    else:
        return JsonResponse({'status': 401, 'error': form.errors()})
