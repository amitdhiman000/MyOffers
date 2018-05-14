from base.forms import (CreateForm, UpdateForm)
from base.validators import (NoValidator, NameValidator, DescriptionValidator)
from base.validators import (EmailValidator, PhoneValidator)
from public.models import Message


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


class MessageForm(CreateForm):

    def __init__(self):
        super().__init__()
        self.m_fields = form_fields

    def validate(self):
        is_valid = super().validate()
        if not is_valid:
            return is_valid
        if self.request().user.is_loggedin() is True:
            self.add_model_value('fk_user', self.request().user)
        return True

    def save(self):
        print('saving ....')
        ret = Message.create_v1(self.model_values())
        return ret[0]
