from myadmin.backenddb import (insert_default_areas, insert_custom_areas, insert_default_categories)

from offer.models import Category
from locus.models import (Country ,State, City, Area)
from mail.models import (PublicMessage)
from myadmin.preload_data import (gCountries, gCategories)
from base.apputil import (App_AdminRequired, App_Render)
# Create your views here.


@App_AdminRequired
def home(request):
    data = {'title': 'MyAdmin'}
    return App_Render(request, 'admin/admin_home_1.html', data)


@App_AdminRequired
def locus_area_view(request, country, state, city, area):
    print(area)
    areas = Area.fetch_by_name(area, city, state, country)
    data = {'title': 'MyAdmin', 'country': country, 'state': state, 'city': city, 'area': area, 'areas': areas}
    return App_Render(request, 'admin/admin_locus_area_1.html', data)


@App_AdminRequired
def locus_city_view(request, country, state, city):
    print(city)
    filter = {'fk_city__name': city, 'fk_state__name': state, 'fk_country__name': country}
    areas = Area.fetch(filter)
    data = {'title': 'MyAdmin', 'country': country, 'state': state, 'city': city, 'areas': areas}
    return App_Render(request, 'admin/admin_locus_city_1.html', data)


@App_AdminRequired
def locus_state_view(request, country, state):
    print(state)
    filter = {'fk_state__name': state, 'fk_country__name': country}
    cities = City.fetch(filter)
    data = {'title': 'MyAdmin', 'country': country, 'state': state, 'cities': cities}
    return App_Render(request, 'admin/admin_locus_state_1.html', data)


@App_AdminRequired
def locus_country_view(request, country):
    print(country)
    states = State.fetch({'fk_country__name': country})
    data = {'title': 'MyAdmin', 'country': country, 'states': states}
    return App_Render(request, 'admin/admin_locus_country_1.html', data)


@App_AdminRequired
def locus_view0(request):
    countries = Country.fetch_all()
    states = State.fetch({'fk_country__name': 'India'})
    data = {'title': 'MyAdmin', 'countries': countries, 'states': states}
    return App_Render(request, 'admin/admin_locus_view_1.html', data)


@App_AdminRequired
def locus_view(request, query=''):
    print('query : '+query)
    params = query.rstrip('/').split('/')
    length = len(params)
    print(params)
    print('length : '+str(length))
    if length == 1 and params[0] != '':
        return locus_country_view(request, params[0])
    elif length == 2:
        return locus_state_view(request, params[0], params[1])
    elif length == 3:
        return locus_city_view(request, params[0], params[1], params[2])
    elif length == 4:
        return locus_area_view(request, params[0], params[1], params[2], params[3])
    return locus_view0(request)


@App_AdminRequired
def locus_country_add_view(request, country):
    states = {}
    if country in gCountries:
        states = gCountries[country]
    data = {'title': 'MyAdmin', 'country': country, 'states': states}
    return App_Render(request, 'admin/admin_locus_country_add_1.html', data)


@App_AdminRequired
def locus_add_view0(request):
    countries = list(gCountries.keys())
    data = {'title': 'MyAdmin', 'countries': countries}
    return App_Render(request, 'admin/admin_locus_add_1.html', data)


@App_AdminRequired
def locus_add_view(request, query=''):
    print('query : '+query)
    params = query.rstrip('/').split('/')
    length = len(params)
    print(params)
    print('length : '+str(length))
    if length == 1 and params[0] != '':
        return locus_country_add_view(request, params[0])
    elif length == 2:
        return locus_state_add_view(request, params[0], params[1])
    elif length == 3:
        return locus_city_add_view(request, params[0], params[1], params[2])
    elif length == 4:
        return locus_area_add_view(request, params[0], params[1], params[2], params[3])
    return locus_add_view0(request)


@App_AdminRequired
def locus_auth(request, query=''):
    print('query : '+query)
    params = query.rstrip('/').split('/')
    length = len(params)
    print(params)
    print('length : '+str(length))
    if length < 3:
        return None

    country = params[0]
    state = params[1]
    city = params[2]
    print(country, state, city)
    if City.fetch_by_name(city_name=city, state_name=state, country_name=country) is None:
        insert_custom_areas(city, state, country)
    areas = Area.fetch_by_city(city)
    data = {'title': 'Location', 'country': country, 'state': state, 'city': city, 'areas': areas}
    return App_Render(request, 'admin/admin_locus_added_1.html', data)


@App_AdminRequired
def category_view(request, query=''):
    print('query : '+query)
    params = query.rstrip('/').split('/')
    length = len(params)
    print(params)
    print('length : '+str(length))

    name = "All"
    if length > 0 and params[0] != '':
        name = params[length - 1]

    categories = Category.fetch_children(name)
    data = {'title': 'MyAdmin', 'categories': categories}
    return App_Render(request, 'admin/admin_category_1.html', data)


@App_AdminRequired
def category_add_view0(request):
    base_cat = gCategories[0]['sub']
    print(len(base_cat))
    data = {'title': 'MyAdmin', 'categories': base_cat}
    return App_Render(request, 'admin/admin_category_add_1.html', data)


@App_AdminRequired
def category_add_view1(request, params, length):
    print(request)
    index = 0
    cat_list = gCategories
    while index < length:
        for cat in cat_list:
            if cat['name'] == params[index]:
                if 'sub' in cat:
                    cat_list = cat['sub']
                else:
                    print('No more subcategories, jump to root')
                    cat_list = cat
                    index = length
                break
        index = index + 1

    nav_links = []
    url = '/myadmin/category-add/'
    for param in params:
        print('param : '+param)
        url += param + "/"
        nav_links.append({'text': param, 'href': url})

    data = {}
    if type(cat_list) is list:
        categories = []
        desired_attrs = ['name', 'desc']
        for cat in cat_list:
            categories.append({ key: value for key,value in cat.items() if key in desired_attrs })
        print(len(categories))
        print(categories)
        data.update({'categories': categories})
    else:
        data.update({'category': cat_list})

    data.update({'title': 'Add Category | MyAdmin', 'nav_links': nav_links, })
    return App_Render(request, 'admin/admin_category_add_1.html', data)


@App_AdminRequired
def category_add(request, params):
    insert_default_categories()


@App_AdminRequired
def category_add_view(request, query):
    print('query : '+query)
    params = query.rstrip('/').split('/')
    length = len(params)
    print(params)
    print('length : '+str(length))
    command = request.GET.get('command', '')
    if command == 'Add':
        category_add(request, params)

    if params[0] == '':
        params[0] = 'All';
    return category_add_view1(request, params, length)


@App_AdminRequired
def messages_view(request):
    print('chaum executing this')
    messages = PublicMessage.fetch_all()
    data = {'title': 'Messages', 'messages': messages}
    return App_Render(request, 'admin/admin_message_1.html', data)
