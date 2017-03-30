from django.conf import settings
from django.shortcuts import render
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt

from offer.models import Offer
from locus.models import Area

##debug
from pprint import pprint
# Create your views here.

@csrf_exempt
def offer(request):
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


