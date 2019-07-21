# from django.conf import settings
from user.models import (UserModel, GuestModel)

USER_UID_KEY = '_user_uid'
USER_EMAIL_KEY = '_user_name'
USER_NAME_KEY = '_user_email'
USER_LEVEL_KEY = '_user_level'
USER_AUTH_KEY = '_user_auth'


def fetch_user(request):
    user = None
    if USER_EMAIL_KEY in request.session:
        uid = request.session[USER_UID_KEY]
        email = request.session[USER_EMAIL_KEY]
        name = request.session[USER_NAME_KEY]
        level = request.session[USER_LEVEL_KEY]
        user = UserModel(id=uid, email=email, name=name, level=level)
    else:
        user = GuestModel()

    # print ('user name : '+user.name)
    return user


def auth_user(email, password):
    return UserModel.check_creds(email, password)


def reload(request, user):
    # need to do it in user.middleware.AuthMiddleware
    newUser  = UserModel.fetch_by_id(user.id)
    request.session[USER_UID_KEY] = newUser.id
    request.session[USER_EMAIL_KEY] = newUser.email
    request.session[USER_NAME_KEY] = newUser.name
    request.session[USER_LEVEL_KEY] = newUser.level
    request.session[USER_AUTH_KEY] = True
    #request.session.set_expiry(60*60)  # 60 minutes session timeout

def login(request, user):
    # need to do it in user.middleware.AuthMiddleware
    request.session[USER_UID_KEY] = user.id
    request.session[USER_EMAIL_KEY] = user.email
    request.session[USER_NAME_KEY] = user.name
    request.session[USER_LEVEL_KEY] = user.level
    request.session[USER_AUTH_KEY] = True
    request.session.set_expiry(60*60)  # 60 minutes session timeout


def logout(request):
    request.session.flush()
    request.user = GuestModel()
    # request._cached_user = request.user
