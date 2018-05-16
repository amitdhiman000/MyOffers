from django.views.generic import TemplateView
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import (csrf_protect)

from mail.forms import PublicMessageForm
from base.apputil import App_Render


def aboutus(request):
    data = {'title': 'About us'}
    return App_Render(request, 'public/public_aboutus_1.html', data)


class ContactsView(TemplateView):
    def get(self, request):
        data = {'title': 'Contacts'}
        return App_Render(request, 'public/public_contacts_1.html', data)

    @method_decorator(csrf_protect)
    def post(self, request):
        print(request.POST)
        error = None
        data = {'title': 'Contacts'}
        form = PublicMessageForm()
        if form.parseForm(request) and form.clean() and form.validate():
            if not form.commit():
                error = form.errors()
        else:
            error = form.errors()

        if request.is_ajax():
            if error is None:
                data.update({'status': 204, 'message': 'Successfuly sent'})
            else:
                data.update({'status': 401, 'message': 'Failed', 'error': error})
            return JsonResponse(data)
        else:
            if error is None:
                return App_Render(request, 'public/public_contacts_sent_1.html', data)
            else:
                request.session['form_errors'] = form.errors()
                request.session['form_values'] = form.values()
            return App_Render(request, 'public/public_contacts_1.html', data)
