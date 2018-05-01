from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from offer.models import Offer
from locus.models import Area


@csrf_exempt
def offer(request):
    key = request.POST.get('key', 'offer')
    offers = Offer.fetch_by_match(key)
    offersdata = list(offers)

    data = {'status': 200, 'data': offersdata}
    print(data)
    return JsonResponse(data)


@csrf_exempt
def location(request):
    print(request.POST)
    key = request.POST.get('key', 'bengaluru')
    areas = Area.fetch_by_match(key)

    areadata = list(areas)
    data = {'status': 200, 'data': areadata}
    return JsonResponse(data)
