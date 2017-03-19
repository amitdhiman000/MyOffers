from django.conf import settings
from django.shortcuts import render
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers

from offer.models import Offer
from user.models import Area

##debug
from pprint import pprint
# Create your views here.

'''
def search(request):
	key = "polls"
	items = ['bengaluru traffic problem', 'vijag city development',
	 'delhi polution and development' ,'election treds in punjab' ,
	 'latest on goa polls']

	matched = ["<li><a>"+item+"</a></li>" for item in items if key in item]

	html = "<ul>"+str("").join(matched)+"</ul>"
	##
	## debug 
	print(html)

	return HttpResponse(html)
'''


@csrf_exempt
def search(request):
	pprint(request.POST)
	key = request.POST.get('key', 'offer')
	offers = Offer.get_match(key)
	offersdata = list(offers)

	data = {'status':200, 'data': offersdata}
	print(data)
	return JsonResponse(data)


@csrf_exempt
def location(request):
	pprint(request.POST)
	key = request.POST.get('key', 'bengaluru')
	areas = Area.get_match(key)

	areadata = list(areas)
	#pprint(areadata)
	data = {'status':200, 'data': areadata}
	return JsonResponse(data)


