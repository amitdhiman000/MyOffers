import base64
from django.db import models
from django.db import connection
from django.utils import timezone
from django.utils.translation import ugettext as _
from django.conf import settings
from datetime import datetime
from django.utils.safestring import mark_safe

from user.models import User

## debug
import traceback
from pprint import pprint
# Create your models here.
