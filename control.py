class BaseControl(object):

	def parseRequest(post):
		return True

	def errors(self):
		return self.m_errors

	def values(self):
		return self.m_values

	def clean(self):
		pass
		#do nothing
		return True

	def validate(self):
		# do nothing
		return True

	def register(self):
		# do nothing
		return None
