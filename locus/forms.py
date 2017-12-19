from common.forms import *
from locus.models import (Area, Address)
from user.models import User

import logging

model_fields = [
    {'name':'id', 'validator': None},
    {'name':'name', 'validator': None},
    {'name':'phone', 'validator': None},
    {'name':'pincode', 'validator': None},
    {'name':'address', 'validator': None},
    {'name':'landmark', 'validator': None},
    {'name':'location', 'validator': None},
]

form_fields = {
    ## form fields
    'A_id': model_fields[0],
    'A_name': model_fields[1],
    'A_phone': model_fields[2],
    'A_pincode': model_fields[3],
    'A_address': model_fields[4],
    'A_landmark': model_fields[5],
    'A_location': model_fields[6],

    ## json fields
    'id': model_fields[0],
    'name': model_fields[1],
    'phone': model_fields[2],
    'pincode': model_fields[3],
    'address': model_fields[4],
    'landmark': model_fields[5],
    'location': model_fields[6],
}


class AddressRegForm(CreateForm):
    model = Address

    def __init__(self):
        super().__init__()
        self.m_fields = form_fields


    def validate(self):
        super().validate()

        location = self.model_value('location')
        if location != '':
            self.del_model_value('location')
            try:
                loc = location.split(',')
                if len(loc) == 2:
                    self.add_model_value('latitude', loc[0])
                    self.add_model_value('longitude', loc[1])
            except Exception as ex:
                logging.error(ex)
                self.set_error('location', 'Failed to parse location')
                self.m_valid = False

        pincode = self.model_value('pincode')
        address = self.model_value('address')
        if pincode != '':
            areas = Area.fetch_by_pincode(pincode)
            final_area = areas.first()
            for area in areas:
                print(area.name, area.pincode)
                if address.find(area.name):
                    final_area = area
            self.add_model_value('fk_area', final_area)
            self.del_model_value('pincode')
        else:
            self.set_error('pincode', 'Pincode is required')


        self.add_model_value('fk_user', self.request().user)

        return self.valid()


    def save(self):
        print(self.model_values())
        return self.model.create(self.model_values())



class AddressUpdateForm(Form):
    model = Address

    def __init__(self):
        super().__init__()
        self.m_fields = form_fields


    def validate(self):
        super().validate()
        return self.valid()


    def update(self):
        return self.model.update(self.model_values())



class AddressDeleteForm(DeleteForm):
    model = Address

    def __init__(self):
        super().__init__()
        self.m_fields = {
			'A_id': {'name':'id', 'validator':None},
			'id': {'name':'id', 'validator':None},
		}


    def validate(self):
        super().validate()
        self.add_model_value('fk_user', self.request().user)
        return self.valid()


    def delete(self):
        print(self.model_values())
        return self.model.remove(self.model_values())
