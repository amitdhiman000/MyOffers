def auth(request):
    """
    Returns context variables required by apps that use Django's authentication
    system.

    If there is no 'user' attribute in the request, uses AnonymousUser (from
    django.contrib.auth).
    """
    print('amit : context_processor')
    if hasattr(request, 'user'):
        user = request.user
    else:
        from user.models import Guest
        user = Guest()

    return {'user': user,}
