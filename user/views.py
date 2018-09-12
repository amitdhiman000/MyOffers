from django.conf import settings
from django.http import JsonResponse

# custom authentication
from user import backends
from user.models import User
from locus.models import Address

from base.apputil import (App_LoginRequired, App_PostRequired, App_RedirectIfLoggedin)
from base.apputil import (App_Render, App_Redirect, App_RunTime)
from base.apputil import App_TokenRequired
from user.services import UserService
from user.forms import (UserRegForm, UserUpdateForm, UserSignInForm)
from api.views import RestApiView


class UserView(RestApiView):
    service = UserService
    form = UserRegForm

    @App_TokenRequired
    def get(self, request, key=None):
        print('user : ', request.user)
        if key is None:
            users = self.service.users()
            return JsonResponse({'result': users}, status=200)
        user = self.service.user_by_id(key)
        if user is None:
            return JsonResponse({'error': {'message': 'Resource not found'}}, status=404)
        return JsonResponse({'result': user}, status=200)

    @App_TokenRequired
    def post(self, request, key=None):
        form = self.form()
        if (form.parseJson(request)
            and form.clean()
            and form.validate()):
            obj = form.save()
            if obj is not None:
                res = JsonResponse(status=201)
                res['location'] = obj.absolute_url()
                return res
        errors = form.errors()
        return JsonResponse(errors, status=400)


def home_view(request):
    return user_account_view(request)


@App_RedirectIfLoggedin
def signin_view(request):
    data = {'title': 'Login'}
    if 'form_errors' in request.session:
        data['form_errors'] = request.session['form_errors']
        data['form_values'] = request.session['form_values']
        del request.session['form_errors']
        del request.session['form_values']

    data.update({settings.USER_LOGIN_NEXT: request.GET.get(settings.USER_LOGIN_NEXT, settings.HOME_URL)})
    return App_Render(request, 'user/user_signin_1.html', data)


# functions for registration
@App_RedirectIfLoggedin
def signup_view(request):
    data = {'title': 'Signup'}
    data.update({settings.USER_LOGIN_NEXT: request.POST.get(settings.USER_LOGIN_NEXT, settings.HOME_URL)})
    if 'form_errors' in request.session:
        data['form_errors'] = request.session['form_errors']
        data['form_values'] = request.session['form_values']
        del request.session['form_errors']
        del request.session['form_values']

    return App_Render(request, 'user/user_signup_1.html', data)


@App_PostRequired
def signin_auth(request):
    print(request.POST)
    form = UserSignInForm()
    if (form.parseForm(request)
            and form.clean()
            and form.validate()):
        user = form.commit()
        if user is not None:
            print(settings.USER_LOGIN_NEXT)
            print(settings.HOME_URL)
            redirect_url = request.POST.get(settings.USER_LOGIN_NEXT, settings.HOME_URL)
            print('redirect_url : ', redirect_url)
            return App_Redirect(request, redirect_url)

    # Only error case will reach here.
    if request.is_ajax():
        error = form.errors()
        return JsonResponse({'status': 401, 'message': 'SignIn failed', 'data': error})
    else:
        redirect_url = request.META.get('HTTP_REFERER', settings.USER_LOGIN_URL)
        request.session['form_errors'] = form.errors()
        request.session['form_values'] = form.values()
        return App_Redirect(request, redirect_url)


@App_PostRequired
def signup_auth(request):
    print(request.POST)
    form = UserRegForm()
    if (form.parseForm(request)
            and form.clean()
            and form.validate()):
        user = form.commit()
        if user is not None:
            print('registration successful')
            backends.login(request, user)
            return App_Redirect(request, settings.USER_SIGNUP_SUCCESS_URL)

    error = form.errors()
    if request.is_ajax():
        return JsonResponse({'status': 401, 'message': 'Signup Failed!!', 'data': error})
    else:
        request.session['form_errors'] = error
        request.session['form_values'] = form.values()
        return App_Redirect(request, settings.USER_SIGNUP_URL)


@App_LoginRequired
def signup_success_view(request):
    print('registration success')
    data = {'title': 'Signup | Success'}
    return App_Render(request, 'user/user_registered_1.html', data)


def signout(request):
    backends.logout(request)
    return App_Redirect(request, settings.USER_LOGIN_URL)


@App_RunTime
@App_LoginRequired
def user_account_view(request):
    user = User.fetch_user(request.user)
    address = Address.fetch_by_user(user)
    user.address = address
    data = {'title': 'Account', 'user': user}
    return App_Render(request, 'user/user_account_1.html', data)


@App_LoginRequired
def user_messages_view(request):
    print(request.GET.urlencode())
    data = {'title': 'User mails'}
    return App_Render(request, 'user/user_messages_1.html', data)


@App_LoginRequired
def user_stats_view(request):
    data = {'title': 'User stats'}
    return App_Render(request, 'user/user_stats_1.html', data)


@App_LoginRequired
def user_wishlist_view(request):
    data = {'title': 'User Wishlist'}
    return App_Render(request, 'user/user_wishlist_1.html', data)


@App_LoginRequired
def user_settings_view(request):
    data = {'title': 'User settings'}
    return App_Render(request, 'user/user_settings_1.html', data)


@App_LoginRequired
def user_update(request):
    data = None
    form = UserUpdateForm()
    if (form.parseForm(request)
            and form.clean()
            and form.validate()):
        data = form.commit()

    # update user info in ongoing session
    if data:
        backends.reload(request, request.user)
        

    if request.is_ajax():
        if data is None:
            return JsonResponse({'status': 400, 'message': 'Save Failed', 'data': form.errors()})
        else:
            return JsonResponse({'status': 200, 'message': 'Saved Successfully', 'data': form.result()})
    else:
        return App_Redirect(request)


@App_LoginRequired
def user_topic_selected(request):
    print(request.POST)
    error = None
    msg = None
    topic_id = request.POST.get('topic_id', -1)
    topic_followed = int(request.POST.get('topic_followed', 0))
    if topic_followed == 0:
        if TopicFollower.fetch_follower(request.user, topic_id):
            msg = 'folllowed'
        else:
            error = 'Server operation failed'
    elif topic_followed == 1:
        if TopicFollower.remove_follower(request.user, topic_id):
            msg = 'unfollowed'
        else:
            error = 'Server operation failed'
    else:
        error = 'Invalid request'

    # send the response
    if request.is_ajax():
        if error is None:
            return JsonResponse({'status': 204, 'message': msg, 'data': {}})
        else:
            return JsonResponse({'status': 401, 'message': 'Server Error', 'data': error})
    else:
        return App_Redirect(request)
