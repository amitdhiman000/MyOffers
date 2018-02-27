from django.views.decorators.csrf import (csrf_protect, csrf_exempt)
from business.models import (Category, Business)
from business.services import BusinessService
from business.forms import *
from base.apputil import *

# Create your views here.

@App_RunTime
@App_LoginRequired
def business_home_view(request):
	business = Business.fetch_by_user(request.user)
	categories = Category.fetch_first_level()
	data = {'title': 'My Business', 'business': business, 'categories': categories };
	return App_Render(request, 'business/business_1.html', data)


@App_LoginRequired
def business_create(request):
	data = None
	print(request.POST)
	form = BusinessRegForm()
	if (form.parseForm(request)
			and form.clean()
			and form.validate()):
		data = form.commit()
		#data = model_to_dict(data)

	if request.is_ajax:
		if data != None:
			categories = Category.fetch_first_level()
			return App_Render(request, 'business/business_item_1.html', {'b':data, 'categories':categories})
			##return JsonResponse({'status':200, 'message':'Business saved', 'data':data});
		else:
			data = form.errors()
			return JsonResponse({'status':401, 'message':'Business save failed', 'data':data});
	else:
		return App_Redirect(request)

@csrf_protect
@App_LoginRequired
def business_update(request):
	print(request.POST)
	data = None
	form = BusinessUpdateForm()
	if (form.parseForm(request)
			and form.clean()
			and form.validate()):
		data = form.commit()

	if request.is_ajax:
		if data != None:
			return JsonResponse({'status':200, 'message':'Business updated', 'data':data});
		else:
			data = form.errors()
			return JsonResponse({'status':401, 'message':'Business update failed', 'data':data});
	else:
		return App_Redirect(request)


@App_LoginRequired
def business_delete(request):
	data = {'title': 'My Business'};
	return App_Render(request, 'business/business_1.html', data)


@App_LoginRequired
def business_address_view(request):

	b_id = request.POST.get('business_id', -1)
	data = BusinessService.fetch_by_business(b_id, request.user)
	print(data)
	if request.is_ajax:
		if data != None:
			return App_Render(request, 'business/business_address_2.html', {'addresses':data})
		else:
			return JsonResponse({'status':401, 'message':'Business save failed', 'data':{'error': 'Failed to fetch addresses'}});
	else:
		return App_Redirect(request)


@App_LoginRequired
def business_address_link(request):
	print(request)
	print(request.POST)

	data = None
	form = BALinkForm()

	if request.is_ajax:
		if data != None:
			return JsonResponse({'status':200, 'message':'Address linked', 'data':data});
		else:
			data = form.errors()
			return JsonResponse({'status':401, 'message':'Address linking failed', 'data':data});
	else:
		return App_Redirect(request)


@App_LoginRequired
def business_address_unlink(request):
	data = None
	control = AddressControl()
	if (control.parseRequest(request)
			and control.clean()
			and control.validate()):
		data = control.execute()
		#data = model_to_dict(data)

	if request.is_ajax:
		if data != None:
			categories = Category.fetch_first_level()
			return App_Render(request, 'business/business_item_1.html', {'b':data, 'categories':categories})
			##return JsonResponse({'status':200, 'message':'Business saved', 'data':data});
		else:
			data = control.errors()
			return JsonResponse({'status':401, 'message':'Business save failed', 'data':data});
	else:
		return App_Redirect(request)
