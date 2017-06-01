def user(request):
    """
    Returns context variables required by apps that use Django's authentication
    system.

    If there is no 'user' attribute in the request, uses AnonymousUser (from
    django.contrib.auth).
    """
    if hasattr(request, 'user'):
        user = request.user
    else:
        from user.models import Guest
        user = Guest()

    return {'user': user,}

def ajax(request):
    return {'is_ajax': request.is_ajax()}
