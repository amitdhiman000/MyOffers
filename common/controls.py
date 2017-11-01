class BaseControl(object):
	m_valid = True
	m_errors = {}
	m_values = {}

	def parseRequest(self, request):
		return True

	def errors(self):
		return self.m_errors

	def values(self):
		return self.m_values

	def clean(self):
		#do nothing
		return True

	def validate(self):
		# do nothing
		return True

	def execute(self):
		# do nothing
		return None
