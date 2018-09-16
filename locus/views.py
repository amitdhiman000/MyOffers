from django.template.context_processors import csrf
from django.views.decorators.csrf import (csrf_protect, csrf_exempt)
from django.utils.decorators import method_decorator
from django.http import HttpResponse, JsonResponse

from base.apputil import *
from locus.forms import (AddressCreateForm, AddressUpdateForm, AddressDeleteForm)
from locus.services import AddressService
from api.views import RestApiView

import logging


class AddressView(RestApiView):
    form = AddressCreateForm
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
        if key is None:
            addresses = self.service.address()
            return JsonResponse({'result':addresses})

        address = self.service.address_by_id(key)
        if address is None:
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
            if obj is not None:
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


@App_RunTime
@App_LoginRequired
def address_view(request):
    addresses = AddressService.address_by_user(request.user)
    print(addresses)
    #print(addresses[0]['url'])
    data = {'title': 'Address', 'addresses': addresses}
    return App_Render(request, 'locus/address_1.html', data)


@App_LoginRequired
def address_create(request):
    aid = request.POST.get('A_id', '-1')
    if (aid != '-1'):
        return address_update(request)

    data = None
    form = AddressCreateForm()
    if (form.parseForm(request)
        and form.clean()
        and form.validate()):
        data = form.commit()

    if request.is_ajax():
        if data is not None:
            data = AddressService.address_by_id(data.id)
            return App_Render(request, 'locus/address_item_1.html', {'address': data})
        else:
            data = form.errors()
            return JsonResponse({'status': 400, 'message': 'Address saving failed', 'data': data})
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
        if data is not None:
            return JsonResponse({'status': 200, 'message': 'Address updated', 'data': data})
        else:
            data = form.errors()
            return JsonResponse({'status': 400, 'message': 'Address update failed', 'data': data})
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
        if data is not None:
            return JsonResponse({'status': 200, 'message': 'Address updated', 'data': data})
        else:
            data = form.errors()
            return JsonResponse({'status': 400, 'message': 'Address update failed', 'data': data})
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
        if data is True:
            return JsonResponse({'status': 204, 'message': 'Address deleted'})
        else:
            data = form.errors()
            return JsonResponse({'status': 400, 'message': 'Address delete failed', 'data': data})
    return App_Redirect(request)
