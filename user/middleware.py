from django.utils.functional import SimpleLazyObject
from . import backends


def fetch_user(request):
    if not hasattr(request, '_cached_user'):
        request._cached_user = backends.fetch_user(request)
    return request._cached_user


class AuthMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        assert hasattr(request, 'session'), (
            "The Django authentication middleware requires session middleware "
            "to be installed. Edit your MIDDLEWARE_CLASSES setting to insert "
            "'django.contrib.sessions.middleware.SessionMiddleware' before "
            "'django.contrib.auth.middleware.AuthenticationMiddleware'."
        )
        request.user = SimpleLazyObject(lambda: fetch_user(request))
        response = self.get_response(request)
        return response

    # this method will suppress the excepion callstack so commented
    # def process_exception(self, request, exception):
    #    pass
