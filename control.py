class BaseControl(object):

	def parseRequest(post):
		return True

	def get_errors(self):
		return self.m_errors

	def get_values(self):
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
