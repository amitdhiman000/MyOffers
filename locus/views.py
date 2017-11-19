from django.template.context_processors import csrf
from common.apputil import *
from locus.controls import *
from locus.models import Address
# Create your views here.


@App_LoginRequired
def home_view(request):
    addresses = Address.fetch_by_user(request.user)
    data = {'title': 'Address', 'addresses': addresses}
    data.update(csrf(request))
    return App_Render(request, 'locus/address_1.html', data)


@App_LoginRequired
def address_view(request):
    addresses = Address.fetch_by_user(request.user)
    data = {'title': 'Address', 'addresses': addresses}
    data.update(csrf(request))
    return App_Render(request, 'locus/address_1.html', data)


@App_LoginRequired
def address_create(request):
    data = None
    control = AddressControl()
    if (control.parseRequest(request)
        and control.clean()
        and control.validate()):
        data = control.execute()

    data = control.errors()
    if request.is_ajax():
        if data != None:
            return JsonResponse({'status': 200, 'message': 'Saved Successfully', 'data': data})
        else:
            data = control.errors()
            return JsonResponse({'status': 400, 'message': 'Saving Failed', 'data': data})
    return App_Redirect(request, '/locus/address/')


@App_LoginRequired
def address_update(request):
    data = None
    control = AddressControl()
    if (control.parseRequest(request)
        and control.clean()
        and control.validate()):
        data = control.execute()

    data = control.errors()
    if request.is_ajax():
        if data != None:
            return JsonResponse({'status': 200, 'message': 'Saved Successfully', 'data': data})
        else:
            data = control.errors()
            return JsonResponse({'status': 400, 'message': 'Saving Failed', 'data': data})
    return App_Redirect(request, '/locus/address/')


@App_LoginRequired
def address_delete(request):
    logging.error(request.POST)
    error = None
    id = request.POST.get('id', -1)
    if Address.remove(id, request.user) == False:
        error = {'error': 'Failed to delete'}
    if request.is_ajax():
        if error == None:
            return JsonResponse({'status': 204, 'message': 'Deleted Successfully'})
        else:
            return JsonResponse({'status': 400, 'message': 'Deletion Failed', 'data': error})
    return App_Redirect(request, '/locus/address/')
