from base.forms import (Form, CreateForm, UpdateForm)
from base.validators import (NoValidator, NameValidator, PasswordValidator)
from base.validators import (EmailValidator, PhoneValidator)
from user.models import User
from user import backends


model_fields = {
    'id': {'name': 'id', 'validator': NoValidator},
    'name': {'name': 'name', 'validator': NameValidator},
    'pass': {'name': 'password', 'validator': PasswordValidator},
    'email': {'name': 'email', 'validator': EmailValidator},
    'phone': {'name': 'phone', 'validator': PhoneValidator},
}

form_fields = {
    # for html form
    'U_id': model_fields['id'],
    'U_name': model_fields['name'],
    'U_pass': model_fields['pass'],
    'U_email': model_fields['email'],
    'U_phone': model_fields['phone'],
    # for json
    'id': model_fields['id'],
    'name': model_fields['name'],
    'pass': model_fields['pass'],
    'email': model_fields['email'],
    'phone': model_fields['phone'],
}


class UserRegForm(CreateForm):

    def __init__(self):
        super().__init__()
        self.m_fields = form_fields

    def validate(self):
        is_valid = super().validate()
        if not is_valid:
            return is_valid
        email = self.model_value('email')
        if User.check_email(email):
            self.set_error('email', 'Account already exist with this Email Id')
            return False
        return True

    def save(self):
        print('saving ....')
        return User.create(self.model_values())


class UserUpdateForm(UpdateForm):

    def __init__(self):
        super().__init__()
        self.m_fields = form_fields

    def validate(self):
        is_valid = super().validate()
        if not is_valid:
            return is_valid
        self.add_model_value('id', self.m_request.user.id)
        self.del_model_value('password')
        print(self.m_values)
        return True

    def update(self):
        print('saving ....')
        if User.update(self.model_values()):
            return self.result()
        return None


class UserSignInForm(Form):

    def __init__(self):
        super().__init__()
        self.m_fields = {
            'U_email': {'name': 'email', 'validator': None},
            'U_pass': {'name': 'password', 'validator': None},
            'email': {'name': 'email', 'validator': None},
            'pass': {'name': 'password', 'validator': None},
        }

    def validate(self):
        return super().validate()

    def commit(self):
        print('commiting....')
        model_values = self.model_values()
        email = model_values['email']
        passw = model_values['password']
        print(email, passw)
        user = backends.auth_user(email, passw)
        if (user is not None):
            backends.login(self.request(), user)
        else:
            self.set_error('email', 'Email or password is wrong!!')
        return user


class UserPasswordUpdateForm(UpdateForm):
    def __init__(self):
        super().__init__()
        self.m_fields = {
            'U_pass0': {'name': 'pass0', 'validator': NoValidator},
            'pass0': {'name': 'pass0', 'validator': NoValidator},
            'U_pass1': model_fields['pass'],
            'pass1': model_fields['pass'],
        }

    def validate(self):
        is_valid = super().validate()
        if not is_valid:
            return is_valid
        user = self.request().user
        old_pass = self.del_model_value('pass0')
        if User.check_password(old_pass, user) or User.check_otp(old_pass, user):
            self.add_model_value('id', self.m_request.user.id)
            print(self.m_values)
        else:
            is_valid = False
            self.set_error('pass0', 'Old password in wrong, not working?, try OTP')
        return is_valid

    def update(self):
        print('saving ....')
        if User.update(self.model_values()):
            self.add_model_value('pass0', 'xxxxxxxxxxx')
            self.add_model_value('password', 'xxxxxxxxxxx')
            return self.result()
        return None