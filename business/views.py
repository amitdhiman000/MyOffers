from django.http import JsonResponse
from django.views.decorators.csrf import (csrf_protect)
from business.models import (Category, Business)
from business.services import BusinessService
from business.forms import (BALinkBulkForm, BAUnLinkForm)
from business.forms import (BusinessRegForm, BusinessUpdateForm, BusinessDeleteForm)
from base.apputil import (App_RunTime, App_Render, App_Redirect)
from base.apputil import (App_LoginRequired, App_GetRequired, App_PostRequired)


@App_RunTime
@App_LoginRequired
def business_home_view(request):
    business = Business.fetch_by_user(request.user)
    categories = Category.fetch_first_level()
    data = {'title': 'My Business', 'business': business, 'categories': categories}
    return App_Render(request, 'business/business_1.html', data)


@App_LoginRequired
def business_create(request):
    print(request.POST)
    data = None

    form = BusinessRegForm()
    if (form.parse(request)
            and form.clean()
            and form.validate()):
        data = form.commit()

    if request.is_ajax:
        if data is not None:
            categories = Category.fetch_first_level()
            return App_Render(request, 'business/business_item_1.html', {'b': data, 'categories': categories})
            # ##return JsonResponse({'status':200, 'message':'Business saved', 'data': data});
        else:
            data = form.errors()
            return JsonResponse({'status': 401, 'message': 'Business save failed', 'data': data})
    else:
        return App_Redirect(request)


@csrf_protect
@App_LoginRequired
def business_update(request):
    print(request.POST)
    data = None

    form = BusinessUpdateForm()
    if (form.parse(request)
            and form.clean()
            and form.validate()):
        data = form.commit()

    if request.is_ajax:
        if data is not None:
            return JsonResponse({'status': 200, 'message': 'Business updated', 'data': data})
        else:
            data = form.errors()
            return JsonResponse({'status': 401, 'message': 'Business update failed', 'data': data})
    else:
        return App_Redirect(request)


@App_LoginRequired
def business_delete(request):
    data = {'title': 'My Business'}
    status = False

    form = BusinessDeleteForm()
    if (form.parse(request)
            and form.clean()
            and form.validate()):
        status = form.commit()

    if request.is_ajax:
        if status:
            return JsonResponse({'status': 204, 'message': 'Deleted Successfully'})
        else:
            data = form.errors()
            return JsonResponse({'status': 401, 'message': 'Delete Failed', 'data': data})
    return App_Render(request, 'business/business_1.html', data)


@App_GetRequired
@App_LoginRequired
def business_address_view(request):
    print(request.GET)
    b_id = request.GET.get('B_id', -1)
    data = BusinessService.fetch_by_business(b_id, request.user)
    print(data)
    if request.is_ajax:
        if data is not None:
            return App_Render(request, 'business/business_address_2.html', {'business': b_id, 'addresses': data})
        else:
            return JsonResponse({'status': 401, 'message': 'Business save failed', 'data': {'error': 'Failed to fetch addresses'}})
    else:
        return App_Redirect(request)


@App_PostRequired
@App_LoginRequired
def business_address_link(request):
    print(request.POST)
    data = None
    form = BALinkBulkForm()

    if (form.parse(request)
            and form.clean()
            and form.validate()):
        data = form.commit()

    if request.is_ajax:
        if data is not None:
            return JsonResponse({'status': 200, 'message': 'Address linked', 'data': data})
        else:
            data = form.errors()
            return JsonResponse({'status': 401, 'message': 'Address linking failed', 'data': data})
    else:
        return App_Redirect(request)


@App_LoginRequired
def business_address_unlink(request):
    data = None
    form = BAUnLinkForm()

    if request.is_ajax:
        if data is not None:
            return JsonResponse({'status': 200, 'message': 'Address unlinked', 'data': data})
        else:
            data = form.errors()
            return JsonResponse({'status': 401, 'message': 'Address unlinked', 'data': data})
    else:
        return App_Redirect(request)
