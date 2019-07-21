from django.views.decorators.csrf import (csrf_exempt)
from offer.models import OfferModel
from offer.views import offer_home_view


def home_view(request):
    return offer_home_view(request)


@csrf_exempt
def test_view(request):
    print(request.POST, request.FILES)
    data = {'title': 'Test Page'}
    method = request.META.get('REQUEST_METHOD', '')
    print(method)
    if method == 'POST':
        for key in request.FILES:
            file = request.FILES[key]
            path = App_SaveUploadedFile(request, file)

    return App_Render(request, 'home/home_test_1.html', data)


def home_backup_view(request):
    offers = OfferModel.get_all()
    data = {'title': 'Home Backup', 'offers_list': offers}
    return App_Render(request, 'home/home_backup_1.html', data)
