from django.template.context_processors import csrf
from django.views.decorators.csrf import (csrf_protect, csrf_exempt)
from django.utils.decorators import method_decorator
from django.http import HttpResponse, JsonResponse

from common.apputil import *
from locus.forms import (AddressRegForm, AddressUpdateForm, AddressDeleteForm)
from locus.services import AddressService
from api.views import RestApiView

import logging


class AddressView(RestApiView):
    form = AddressRegForm
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
    return address_view(request)


@App_LoginRequired
def address_view(request):
    addresses = AddressService.address_by_user(request.user)
    print(len(addresses))
    print(addresses)
    data = {'title': 'Address', 'addresses': addresses}
    return App_Render(request, 'locus/address_1.html', data)


@App_LoginRequired
def address_create(request):
    data = None
    form = AddressRegForm()
    if (form.parseForm(request)
        and form.clean()
        and form.validate()):
        data = form.commit()

    if request.is_ajax():
        if data != None:
            resp = App_Render(request, '/locus/address_item_1.html', {'addresses': list(data)})
            return JsonResponse({'status': 204, 'message': 'Saved Successfully', 'data': resp})
        else:
            data = form.errors()
            return JsonResponse({'status': 400, 'message': 'Saving Failed', 'data': data})
    return App_Redirect(request)


@App_LoginRequired
def address_update(request):
    data = None
    form = AddressUpdateForm()
    if (form.parseForm(request)
        and form.clean()
        and form.validate()):
        data = form.commit()

    data = form.errors()
    if request.is_ajax():
        if data != None:
            return JsonResponse({'status': 200, 'message': 'Saved Successfully', 'data': data})
        else:
            data = form.errors()
            return JsonResponse({'status': 400, 'message': 'Saving Failed', 'data': data})
    return App_Redirect(request)


@App_LoginRequired
def address_patch(request):
    data = None
    form = AddressUpdateForm()
    if (form.parseForm(request)
        and form.clean()
        and form.validate()):
        data = form.commit()

    if request.is_ajax():
        if data != None:
            return JsonResponse({'status': 200, 'message': 'Saved Successfully', 'data': data})
        else:
            data = form.errors()
            return JsonResponse({'status': 400, 'message': 'Saving Failed', 'data': data})
    return App_Redirect(request)


@App_LoginRequired
def address_delete(request):
    logging.error(request.POST)
    form = AddressDeleteForm()
    if (form.parseForm(request)
        and form.clean()
        and form.validate()):
        data = form.commit()

    if request.is_ajax():
        if data == True:
            return JsonResponse({'status': 204, 'message': 'Deleted Successfully'})
        else:
            data = form.errors()
            return JsonResponse({'status': 400, 'message': 'Deletion Failed', 'data': data})
    return App_Redirect(request)
