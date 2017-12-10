
class ValueCleaner(object):
    def __call__(self, value):
        if value == None:
            return value
        return value.strip(' \t\n\r')
