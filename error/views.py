from base.apputil import App_Render


def index(request):
    data = {'title': 'Error'}
    # return HttpResponse ('This is Invalid Request')
    return App_Render(request, 'error/error_error_1.html', data)


def access_denied_view(request):
    data = {'title': 'Access Denied'}
    return App_Render(request, 'error/error_access_denied_1.html', data)


def invalid_request_view(request):
    data = {'title': 'Invalid Request'}
    return App_Render(request, 'error/error_invalid_request_1.html', data)


def under_construction_view(request):
    data = {'title': 'Under Construction'}
    return App_Render(request, 'error/error_under_construction_1.html', data)
