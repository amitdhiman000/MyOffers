from base.forms import (CreateForm, UpdateForm, DeleteForm)
from base.validators import (NoValidator, DescriptionValidator, WebsiteValidator)
from business.validators import (BusinessNameValidator, BusinessCategoryValidator)
from business.services import BusinessService
from locus.models import AddressModel
from business.models import (BusinessModel, CategoryModel, BusinessAddressMapModel)
import logging


model_fields = {
    'id': {'name': 'id', 'validator': NoValidator},
    'name': {'name': 'name', 'validator': BusinessNameValidator},
    'about': {'name': 'about', 'validator': DescriptionValidator},
    'website': {'name': 'website', 'validator': WebsiteValidator},
    'category': {'name': 'fk_category', 'validator': BusinessCategoryValidator},
}

form_fields = {
    # for html form
    'B_id': model_fields['id'],
    'B_name': model_fields['name'],
    'B_about': model_fields['about'],
    'B_website': model_fields['website'],
    'B_category': model_fields['category'],
    # for json
    'id': model_fields['id'],
    'name': model_fields['name'],
    'about': model_fields['about'],
    'website': model_fields['website'],
    'category': model_fields['category'],
}


class BusinessRegForm(CreateForm):

    def __init__(self):
        super().__init__()
        self.m_fields = form_fields

    def validate(self):
        is_valid = super().validate()
        if not is_valid:
            return is_valid

        cat = CategoryModel.fetch_by_id(self.model_value('fk_category'))
        if cat is not None:
            self.add_model_value('fk_category', cat)
        else:
            self.set_error('fk_category', 'Category not found')

        self.add_model_value('fk_user', self.request().user)
        return self.valid()

    def save(self):
        print('saving ....')
        print(self.model_values())
        result = BusinessModel.create_v1(self.model_values())
        if result[1] is False:
            self.set_error('error', 'Business already exists!!')
            return None
        return result[0]


class BusinessUpdateForm(UpdateForm):

    def __init__(self):
        super().__init__()
        self.m_fields = form_fields

    def validate(self):
        is_valid = super().validate()
        if not is_valid:
            return is_valid
        print(self.m_model_values)
        return True

    def update(self):
        print('saving ....')
        if BusinessModel.update(self.model_values()):
            return self.result()
        else:
            return None


class BusinessDeleteForm(DeleteForm):

    def __init__(self):
        super().__init__()
        self.m_fields = {
            'B_id': {'name': 'id', 'validator': None},
            'id': {'name': 'id', 'validator': None},
        }

    def validate(self):
        super().validate()
        if self.model_value('id') is not None:
            self.add_model_value('fk_user', self.request().user)
        else:
            self.set_error('error', 'Invalid request without business id')
        return self.valid()

    def commit(self):
        print(self.model_values())
        if BusinessModel.remove(self.model_values()):
            return True
        else:
            self.set_error('id', 'Failed to delete Bunisess!!')
        return False


ba_fields = {
    'B_id': {'name': 'fk_business', 'validator': NoValidator},
    'A_id': {'name': 'fk_address', 'validator': NoValidator},
    'business_id': {'name': 'fk_business', 'validator': NoValidator},
    'address_id': {'name': 'fk_address', 'validator': NoValidator},
}


class BALinkForm(CreateForm):
    def __init__(self):
        super().__init__()
        self.m_fields = ba_fields

    def validate(self):
        is_valid = super().validate()
        if not is_valid:
            return is_valid

        return self.valid()

    def save(self):
        print('saving ....')
        print(self.model_values())
        return BusinessModel.create(self.model_values())


class BAUnLinkForm(CreateForm):
    def __init__(self):
        super().__init__()
        self.m_fields = ba_fields

    def validate(self):
        is_valid = super().validate()
        if not is_valid:
            return is_valid

        return self.valid()

    def delete(self):
        print('saving ....')
        print(self.model_values())
        return BusinessModel.remove(self.model_values())


ba_fields = {
    'B_id': {'name': 'fk_business', 'validator': NoValidator},
    'A_ids': {'name': 'addresses', 'validator': NoValidator},
    'business_id': {'name': 'fk_business', 'validator': NoValidator},
    'address_ids': {'name': 'addresses', 'validator': NoValidator},
}


class BALinkBulkForm(CreateForm):
    def __init__(self):
        super().__init__()
        self.m_fields = ba_fields

    # overriding parse for special case of list
    def parse(self, request):
        super().parse(request)
        rkey = self.m_rfields.get('addresses', None)
        values_set = self.m_values.getlist(rkey)
        self.make_model_value(rkey, values_set)
        return True

    def clean(self):
        try:
            addresses = self.model_value('addresses')
            addresses.remove('-1')
            addresses = set(map(int, addresses))
            self.add_model_value('addresses', addresses)
            return True
        except Exception as ex:
            logging.error('failed to clean data' + ex)
            self.set_error('addresses', 'Invalid address references')
        return False

    def save(self):
        print('saving ....')
        try:
            b_id = self.model_value('fk_business')
            addresses = self.del_model_value('addresses')

            old_set = set(addresses)
            new_set = BusinessService.fetch_by_linked(b_id, self.request().user)
            insert_set = old_set - new_set
            delete_set = new_set - old_set

            print('insert_set : ', insert_set)
            print('delete_set : ', delete_set)

            business = BusinessModel(id=int(b_id))
            self.add_model_value('fk_business', business)

            for item in insert_set:
                self.add_model_value('fk_address', Address(id=int(item)))
                print(self.model_values())
                BusinessAddressMapModel.create(self.model_values())

            for item in delete_set:
                self.add_model_value('fk_address', Address(id=int(item)))
                print(self.model_values())
                BusinessAddressMapModel.remove(self.model_values())
            return True
        except Exception as ex:
            logging.error(ex)
            self.set_error('addresses', 'Failed to link/unlink address')
        return False
