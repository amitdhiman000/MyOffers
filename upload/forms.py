import json
from background_task import background
from upload.models import (FileUploadModel, ImageUploadModel)
from base.forms import CreateForm


# run after 60 seconds
@background(schedule=1*60)
def clear_file_upload(user_id, upload_id):
    print('clear_file_upload :: start')
    FileUploadModel.remove({'id':upload_id, 'fk_user': user})
    print('clear_file_upload :: done')
    # user.email_user('Here is a notification', 'You have been notified')


# run after 60 seconds
@background(schedule=1*60)
def clear_temp_image(user_id, upload_id):
    print('clear_file_upload :: start')
    ImageUploadModel.remove({'id':upload_id})
    print('clear_file_upload :: done')
    # user.email_user('Here is a notification', 'You have been notified')


class FileUploadForm(CreateForm):

    def __init__(self):
        super().__init__()
        self.m_fields = {
            'image': {'name': 'file', 'validator': None},
        }

    def parse(self, request):
        self.m_request = request
        self.m_values = request.FILES

        for key in self.m_values:
            if key in self.m_fields:
                self.make_model_value(key, self.m_values[key])
        return True

    def clean(self):
        return True

    def validate(self):
        super().validate()
        #self.add_model_value('fk_user', self.request().user)
        return self.valid()

    def commit(self):
        print(self.model_values())
        upload = FileUploadModel.create(self.model_values())
        if upload:
            pass
            # clear_file_upload(self.request().user.id, upload.id)
        else:
            self.set_error('upload', 'File save server error, try again')
        return upload


class ImageUploadForm(CreateForm):

    def __init__(self):
        super().__init__()

    def parse(self, request):
        self.m_request = request
        self.m_values = request.FILES
        return True

    def clean(self):
        return True

    def validate(self):
        return True

    def commit(self):
        values = self.values()
        print(values)
        uploads = []
        for key in values:
            model_values = {'file': values[key]}
            upload = ImageUploadModel.create(model_values)
            uploads.append(upload.id)
    
        if uploads:
            pass
            # clear_file_upload(self.request().user.id, upload.id)
        else:
            self.set_error('upload', 'File save server error, try again')
        return uploads
