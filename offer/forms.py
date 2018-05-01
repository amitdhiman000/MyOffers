from django.utils import timezone
from datetime import datetime
from base.forms import (CreateForm, UpdateForm, DeleteForm)

from business.models import Business
from locus.models import Address
from offer.models import (Offer, OfferCategoryMap)
from upload.models import FileUpload

from base.validators import (DescriptionValidator, PriceValidator, DiscountValidator, DateValidator)
from offer.validators import OfferNameValidator
from base.apputil import App_Slugify


model_fields = [
    {'name': 'id', 'validator': None},
    {'name': 'name', 'validator': OfferNameValidator},
    {'name': 'image', 'validator': None},
    {'name': 'details', 'validator': DescriptionValidator},
    {'name': 'price', 'validator': PriceValidator},
    {'name': 'discount', 'validator': DiscountValidator},
    {'name': 'discount_price', 'validator': None},
    {'name': 'start_at', 'validator': DateValidator},
    {'name': 'expire_at', 'validator': DateValidator},
    {'name': 'fk_business', 'validator': None},
    {'name': 'fk_user', 'validator': None},
]

form_fields = {
    # form fields
    'OF_id': model_fields[0],
    'OF_name': model_fields[1],
    'OF_image': model_fields[2],
    'OF_details': model_fields[3],
    'OF_price': model_fields[4],
    'OF_discount': model_fields[5],
    'OF_discount_price': model_fields[6],
    'OF_start_date': model_fields[7],
    'OF_expire_date': model_fields[8],
    'OF_business': model_fields[9],

    # json fields
    'id': model_fields[0],
    'name':  model_fields[1],
    'image': model_fields[2],
    'details': model_fields[3],
    'price': model_fields[4],
    'discount': model_fields[5],
    'discount_price': model_fields[6],
    'start_date': model_fields[7],
    'expire_date': model_fields[8],
    'business': model_fields[9],
}


class OfferRegForm(CreateForm):
    model = Offer

    def __init__(self):
        super().__init__()
        self.m_fields = form_fields

    def validate(self):
        super().validate()

        error = None
        start = self.model_value('start_at')
        end = self.model_value('expire_at')
        if start is None or start == '':
            error = ('start_at', '*Date value is missing')
        elif end is None or end == '':
            error = ('expire_at', '*Date value is missing')
        else:
            tz = timezone.get_current_timezone()
            start = tz.localize(datetime.strptime(start, "%Y/%m/%d"))
            if start < timezone.now():
                error = ('start_at', '*Start date cannot be before today')

            end = tz.localize(datetime.strptime(end, "%Y/%m/%d"))
            if end < timezone.now():
                error = ('expire_at', '*Expire date cannot be before today')

            if start > end:
                error = ('start_at', '*Start date cannot be before expire date')

        if error is None:
            self.add_model_value('start_at', start)
            self.add_model_value('expire_at', start)
        else:
            self.set_error(*error)

        files = self.m_values.get('files', '')
        if files != '':
            images = files.split(',')
            # FIXME :: fetch support for multiple images
            upload = FileUpload.fetch_file(images[0], self.request().user)
            if upload is not None:
                self.add_model_value('image', upload.file)
        else:
            self.set_error('fk_business', 'Image not uploaded')

        self.add_model_value('fk_user', self.request().user)
        business_id = self.model_value('fk_business')
        business = Business.fetch_by_id(business_id)
        if business is not None:
            self.add_model_value('fk_business', business)
        else:
            self.set_error('fk_business', 'Business does not exist')

        # compute the slug
        slug = self.model_value('name')+'-by-'+self.request().user.name
        slug = App_Slugify(slug)
        if Offer.fetch_by_slug(slug) is None:
            self.add_model_value('slug', slug)
        else:
            self.set_error('name', '*Offer with same name is already posted by you')

        return self.valid()

    def save(self):
        print('saving ....')
        print(self.model_values())
        offer = self.model.create(self.model_values())
        if offer is not None:
            pass
            # OfferCategoryMap.create({'fk_offer':offer, 'fk_category':offer.fk_business.fk_category})
            # OfferAddressMap.create(offer, offer.fk_business.fk_address)
            # FileUpload.mark_used(self.m_files[0], self.m_user)
        return offer


class OfferUpdateForm(UpdateForm):
    model = Offer

    def __init__(self):
        super().__init__()
        self.m_fields = form_fields

    def validate(self):
        super().validate()
        return self.valid()

    def update(self):
        return self.model.update(self.model_values())


class OfferDeleteForm(DeleteForm):
    model = Address

    def __init__(self):
        super().__init__()
        self.m_fields = {
            'OF_id': {'name': 'id', 'validator': None},
            'id': {'name': 'id', 'validator': None},
        }

    def validate(self):
        super().validate()
        self.add_model_value('fk_user', self.request().user)
        return self.valid()

    def delete(self):
        print(self.model_values())
        return self.model.remove(self.model_values())
