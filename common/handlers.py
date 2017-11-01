class BaseHandler(object):

	def handle(self, request):
		return True

	def errors(self):
		return self.m_errors

	def values(self):
		return self.m_values
