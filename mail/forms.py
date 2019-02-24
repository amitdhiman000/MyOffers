from base.forms import (CreateForm, UpdateForm)
from base.validators import (NoValidator, NameValidator, DescriptionValidator)
from base.validators import (EmailValidator, PhoneValidator)
from mail.models import (PublicMessage, PrivateMessage)


model_fields = {
    'id': {'name': 'id', 'validator': NoValidator},
    'name': {'name': 'name', 'validator': NameValidator},
    'email': {'name': 'email', 'validator': EmailValidator},
    'phone': {'name': 'phone', 'validator': PhoneValidator},
    'title': {'name': 'title', 'validator': NameValidator},
    'text': {'name': 'text', 'validator': DescriptionValidator},
}

form_fields = {
    # for html form
    'C_id': model_fields['id'],
    'C_name': model_fields['name'],
    'C_email': model_fields['email'],
    'C_phone': model_fields['phone'],
    'C_title': model_fields['title'],
    'C_text': model_fields['text'],
    # for json
    'id': model_fields['id'],
    'name': model_fields['name'],
    'email': model_fields['email'],
    'phone': model_fields['phone'],
    'title': model_fields['title'],
    'text': model_fields['text'],
}


class PublicMessageForm(CreateForm):

    def __init__(self):
        super().__init__()
        self.m_fields = form_fields


    def save(self):
        print('saving ....')
        ret = PublicMessage.create_v1(self.model_values())
        if ret is None:
            self.set_error('error', 'Failed to sent message')
        elif not ret[1]:
            self.set_error('error', 'Duplicate message')
        return ret[1]
