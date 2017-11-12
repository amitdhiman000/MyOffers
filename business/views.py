from business.models import Category
from business.models import Business

from locus.controls import AddressControl
from business.controls import *
from user.controls import *
from common.apputil import *

# Create your views here.

@App_LoginRequired
def business_home_view(request):
	business = Business.fetch_by_user(request.user)
	categories = Category.fetch_first_level()
	data = {'title': 'My Business', 'business': business, 'categories': categories };
	return App_Render(request, 'business/business_1.html', data)


@App_LoginRequired
def business_create(request):
	data = None
	control = BusinessControl()
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
		return App_Redirect(request, '/business/')


@App_LoginRequired
def business_update(request):
	data = None
	control = BusinessControlsFactory.getControl(request)
	if (control.parseRequest(request)
			and control.clean()
			and control.validate()):
		data = control.execute()
		#data = model_to_dict(data)

	if request.is_ajax:
		if data != None:
			return JsonResponse({'status':200, 'message':'Business saved', 'data':data});
		else:
			data = control.errors()
			return JsonResponse({'status':401, 'message':'Business save failed', 'data':data});
	else:
		return App_Redirect(request, '/business/')


@App_LoginRequired
def business_delete(request):
	data = {'title': 'My Business'};
	return App_Render(request, 'business/business_1.html', data)


@App_LoginRequired
def business_address_create(request):
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
		return App_Redirect(request, '/business/')


@App_LoginRequired
def business_address_update(request):
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
		return App_Redirect(request, '/business/')


@App_LoginRequired
def business_address_delete(request):
	data = None
	control = BusinessControl()
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
		return App_Redirect(request, '/business/')
