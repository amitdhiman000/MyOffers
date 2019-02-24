class BaseControl(object):

    def __init__(self):
        self.m_valid = True
        self.m_errors = {}
        self.m_values = {}

    def parseRequest(self, request):
        return False

    def errors(self):
        return self.m_errors

    def values(self):
        return self.m_values

    def reset(self):
        self.m_valid = True
        self.m_errors = {}
        self.m_values = {}
        return self

    def clean(self):
        # do nothing
        return True

    def validate(self):
        # do nothing
        return True

    def execute(self):
        # do nothing
        return None
