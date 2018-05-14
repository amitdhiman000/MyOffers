from django.views.generic import TemplateView
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import (csrf_protect)

from public.forms import MessageForm
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
        form = MessageForm()
        if form.parseForm(request) and form.clean() and form.validate():
            form.commit()
        else:
            error = form.errors()

        if request.is_ajax():
            if error is None:
                data.update({'status': 204, 'message': 'successfuly sent'})
            else:
                data.update({'status': 401, 'error': error})
            return JsonResponse(data)
        else:
            if error is None:
                return App_Render(request, 'public/public_contacts_sent_1.html', data)
            else:
                request.session['form_errors'] = form.errors()
                request.session['form_values'] = form.values()
            return App_Render(request, 'public/public_contacts_1.html', data)
