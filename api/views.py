import json

from django.views import View
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from user.backends import auth_user
from base.apputil import (App_CreateToken, App_RefreshToken)


@csrf_exempt
def token_create(request):
    print(request.POST)
    print(request.body)
    data = json.loads(request.body.decode('utf-8'))
    email = data.get('email', '')
    passw = data.get('pass', '')
    user = auth_user(email, passw)
    if user is not None:
        token = App_CreateToken(request, user)
        if token is not None:
            return JsonResponse({'result': {'token': token}}, status=200)
    return JsonResponse({'result': {'message': 'Email of password is wrong'}}, status=200)


@csrf_exempt
def token_refresh(request):
    token = App_RefreshToken(request, request.user)
    if token is not None:
        return JsonResponse({'result': {'token': token}}, status=200)
    return JsonResponse({'result': {'message': 'Token already expired, login again with email and password'}}, status=200)


class RestApiView(View):
    methods = ('head', 'get', 'post', 'put',
                 'patch', 'delete', 'trace', 'options',
                'copy', 'link', 'unlink', 'lock', 'unlock'
                'purge', 'propfind', 'view', 'connect')

    @classmethod
    def as_view(cls, **kwargs):
        view = super(RestApiView, cls).as_view(**kwargs)
        return csrf_exempt(view)
