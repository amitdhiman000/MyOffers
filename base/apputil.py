import os
import time
import jwt
import base64
from functools import wraps
from django.conf import settings
from django.shortcuts import render
from django.http import (HttpResponseRedirect, JsonResponse)
from django.utils import timezone
from datetime import (datetime, timedelta)
from user_agents import parse


# ##class for mocking any object
# ##
class Klass:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)


# ## JSON Web Token
# ##
def App_CreateToken(request, user):
    if user is None:
        return None
    payload = {'user_id': user.id, 'exp': datetime.utcnow() + timedelta(seconds=600)}
    token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')
    return token.decode('utf-8')


def App_RefreshToken(request, user):
    if user is None:
        return None
    if App_VerifyToken(request):
        return App_CreateToken(request, user)
    return None


def App_VerifyToken(request):
    token = request.META.get('HTTP_AUTHORIZATION', 'a:b')
    print('auth token : ' + token)
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithm='HS256')
        uid = payload['user_id']
        print(uid)
        # request.user = Klass(id=uid)
        return True
    except Exception as e:
        print(e)
    return False


def App_TokenRequired(funct):
    @wraps(funct)
    def _decorator(self, request, *args, **kwargs):
        if App_VerifyToken(request) is False:
            return JsonResponse({'result': {'message': 'Token expired'}}, status=401)
        else:
            return funct(self, request, *args, **kwargs)
    return _decorator


# ## decorator function check for request method,
# ## if not GET redirect to invalid reguest page.
# ##
def App_GetRequired(funct):
    @wraps(funct)
    def _decorator(request, *args, **kwargs):
        if request.method != 'GET':
            return App_Redirect(request, settings.ERROR_INVALID_REQUEST_URL)
        else:
            return funct(request, *args, **kwargs)
    return _decorator


# ## decorator function check for request method,
# ## if not POST redirect to invalid reguest page.
# ##
def App_PostRequired(funct):
    @wraps(funct)
    def _decorator(request, *args, **kwargs):
        if request.method != 'POST':
            return App_Redirect(request, settings.ERROR_INVALID_REQUEST_URL)
            # if 'application/json' in request.META.get('HTTP_ACCEPT'):
        else:
            return funct(request, *args, **kwargs)
    return _decorator


# ## Decorator function for chekcing the login status and redirect to login page
# ##
def App_LoginRequired(funct):
    @wraps(funct)
    def _decorator(request, *args, **kwargs):
        if request.user.is_loggedin() is False:
            redirect_url = settings.USER_LOGIN_URL + "?"+settings.USER_LOGIN_NEXT+"="+request.path
            return App_Redirect(request, redirect_url)
        else:
            return funct(request, *args, **kwargs)
    return _decorator


# ## Decorator function for checking the login user is admin or not
# ##
def App_AdminRequired(funct):
    @wraps(funct)
    def _decorator(request, *args, **kwargs):
        if request.user.is_loggedin() is False:
            return App_Redirect(request, settings.USER_LOGIN_URL)
            # if 'application/json' in request.META.get('HTTP_ACCEPT'):
        elif request.user.level != settings.ADMIN_LEVEL:
            return App_Redirect(request, settings.ERROR_ACCESS_DENIED_URL)
        else:
            return funct(request, *args, **kwargs)
    return _decorator


# ## Decorator function for chekcing the login status and redirect to home page
# ##
def App_RedirectIfLoggedin(funct):
    @wraps(funct)
    def _decorator(request, *args, **kwargs):
        if request.user.is_loggedin() is True:
            return App_Redirect(request, settings.USER_PROFILE_URL)
        return funct(request, *args, **kwargs)
    return _decorator


def App_RunTime(funct):
    @wraps(funct)
    def _decorator(*args, **kwargs):
        t1 = time.time()
        retv = funct(*args, **kwargs)
        t2 = time.time() - t1
        print('{} ran in {} sec'.format(funct.__name__, t2))
        return retv
    return _decorator


# ## return directory path relative media_root
def App_UserFilesDir(user):
    # directory path relative from MEDIA_ROOT  /files/user_<id>/
    directory = os.path.join(settings.MEDIA_USER_FILES_DIR_NAME,
        'user_{0}/'.format(user.id))
    # if not os.path.exists(directory):
    #    os.makedirs(directory)
    # print(directory)
    return directory


# ## return file path relative to media_root
def App_UserFilePath(user, filename):
    filepath = os.path.join(App_UserFilesDir(user),
    '{0}_{1}'.format(timezone.now(), filename))
    print(filepath)
    return filepath


# ## older way of saving uploaded file
def App_SaveUploadedFileOld(request, f):
    directory = App_UserFilesDir(request.user)
    if not os.path.exists(directory):
        os.makedirs(directory)

    filepath = os.path.join(settings.MEDIA_ROOT,
        App_UserFilePath(request.user, f.name))

    with open(filepath, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
    return filepath


# ## new way of saving uploaded file
def App_SaveUploadedFile(request, f):
    from django.core.files.storage import FileSystemStorage
    filedir = os.path.join(settings.MEDIA_ROOT, App_UserFilesDir(request.user))
    fs = FileSystemStorage(location=filedir)
    filename = '{0}_{1}'.format(timezone.now(), f.name)
    fs.save(filename, f)
    # print(filename)
    return filename


def App_Slugify(text):
    import re
    # text = unidecode.unidecode(text).lower()
    return re.sub(r'\W+', '-', text)


def App_Base64Image(file_path):
    filedata = open(file_path, "rb").read()
    text = "{0}{1}".format('data:image/svg+xml;base64,', base64.b64encode(filedata).decode('utf8'))
    # text = "data:image/svg+xml;base64,%s" % base64.b64encode(imgdata).decode('utf8')
    return text


# ## helper functions base to all views
# ##
def App_Template(request, file):
    page_id = request.GET.get('pid', '1')
    ua_string = request.META.get('HTTP_USER_AGENT', '')
    user_agent = parse(ua_string)
    '''
    print(ua_string)
    print(user_agent)
    print(user_agent.is_pc)
    print(user_agent.is_mobile)
    print(user_agent.is_tablet)
    print(user_agent.is_touch_capable)
    print(user_agent.is_bot)
    '''
    base_dir = 'responsive/'
    if user_agent.is_mobile:
        base_dir = 'mobile/'
    else:
        base_dir = 'desktop/'

    base_tpl = None
    if request.is_ajax():
        base_tpl = base_dir + settings.BASE_AJAX_TEMPLATE
    else:
        base_tpl = base_dir + settings.BASE_TEMPLATE

    file_path = base_dir + file[:-6] + page_id + '.html'
    print(base_tpl, file_path, page_id)
    return (base_tpl, file_path)


def App_Redirect(request, url=None):
    if url is None:
        url = request.META.get('HTTP_REFERER', '/')

    if request.is_ajax():
        return JsonResponse({'status': 302, 'url': url})
    return HttpResponseRedirect(url)


def App_Render(request, file, data={'title': settings.APP_NAME}):
    base_tpl, file = App_Template(request, file)
    data.update({'base_template': base_tpl})
    return render(request, file, data)
