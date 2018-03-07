import types

class ValueCleaner(object):
    def __call__(self, value):
        if value == None or type(value) != 'str':
            return value
        return value.strip(' \t\n\r')
