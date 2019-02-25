from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from upload.forms import FileUploadForm
from base.apputil import App_LoginRequired


# User file upload
@csrf_exempt
@App_LoginRequired
def fileupload(request):
    print(request.POST, request.FILES)
    ret = None
    form = FileUploadForm()
    if form.parse(request) and form.clean() and form.validate():
        ret = form.commit()

    if ret is not None:
        return JsonResponse({'status': 200,
            'message': 'successfuly uploaded',
            'data': {'upload_id': ret.id} })
    else:
        return JsonResponse({'status': 401, 'error': form.errors()})
