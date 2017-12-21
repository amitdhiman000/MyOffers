from offer.models import Offer
from offer.views import offer_home_view
from base.apputil import App_Render

from pprint import pprint
# Create your views here.

def home_view(request):
	return offer_home_view(request)


def test_view(request):
	data = {'title': 'Test Page'}
	return App_Render(request, 'home/map_1.html', data)


def home_backup_view(request):
	offers = Offer.get_all()
	data = {'title' : 'Home Backup', 'offers_list': offers}
	return App_Render(request, 'home/home_backup_1.html', data)
