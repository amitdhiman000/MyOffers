from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from offer.models import OfferModel
from locus.models import AreaModel


@csrf_exempt
def offer(request):
    key = request.POST.get('key', 'offer')
    offers = OfferModel.fetch_by_match(key)
    offersdata = list(offers)

    data = {'status': 200, 'data': offersdata}
    print(data)
    return JsonResponse(data)


@csrf_exempt
def location(request):
    print(request.POST)
    key = request.POST.get('key', 'bengaluru')
    areas = AreaModel.fetch_by_match(key)

    areadata = list(areas)
    data = {'status': 200, 'data': areadata}
    return JsonResponse(data)
