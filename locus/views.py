from django.template.context_processors import csrf
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.utils.decorators import method_decorator
from django.http import HttpResponse, JsonResponse

from common.apputil import *
from locus.controls import *
from locus.models import Address

from locus.forms import AddressForm
from locus.services import AddressService

from django.views import View
from api.views import RestApiView

class AddressView(RestApiView):
    form = AddressForm
    service = AddressService

    def head(self, request, key, **kwargs):
        print('head request')
        ts = self.service.timestamp(key)
        response = HttpResponse('')
        # RFC 1123 date format
        response['Last-Modified'] = ts.strftime('%a, %d %b %Y %H:%M:%S GMT')
        return response


    def get(self, request, key=None, *args, **kwargs):
        print('get request')
        if key == None:
            addresses = self.service.address()
            return JsonResponse({'result':addresses})

        address = self.service.address_by_id(key)
        if address == None:
            data = {'error':{'status':404, 'message':'Not Found'}}
            return JsonResponse(data, status=404)
        return JsonResponse(address)


    def post(self, request, *args, **kwargs):
        print('post request')
        print(request.body)
        form = self.form()
        if (form.parseJson(request)
            and form.clean()
            and form.validate()
            ):
            obj = form.save()
            if obj != None:
                res = JsonResponse(status=201)
                res['location'] = obj.absolute_url()
                return res
        errors = form.errors()
        return JsonResponse(errors, status=401)

    def put(self, request, *args, **kwargs):
        print('put request')
        json = request.body
        print(json)
        return JsonResponse({})

    def patch(self, request, *args, **kwargs):
        print('patch request')
        json = request.body
        print(json)
        return JsonResponse({})

    def delete(self, request, *args, **kwargs):
        print('delete request')
        json = request.body
        print(json)
        return JsonResponse({})




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

    if request.is_ajax():
        if data != None:
            return JsonResponse({'status': 204, 'message': 'Saved Successfully'})
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
def address_patch(request):
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
