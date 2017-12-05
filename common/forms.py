class Form(object):

    def __init__(self):
        self._values = {}
        self._errors = {}

    def errors(self):
        return self._errors

    def values(self):
        return self._values

    def clean(self):
        return True

    def validate(self):
        return True

    def save(self):
        return None
