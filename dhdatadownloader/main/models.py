from django.db import models
from django.contrib.auth.models import User

# --------------------------------------- fields.py  --------------------------------------- #

from copy import deepcopy
from base64 import b64encode, b64decode
from zlib import compress, decompress
# try:
#     from cPickle import loads, dumps
# except ImportError:
#     from pickle import loads, dumps

from django.db import models
from django.utils.encoding import force_unicode
from picklefield.fields import PickledObjectField


class DHPhoto(models.Model):
	description = models.CharField(max_length=200)
	level = models.IntegerField()
	userID = models.CharField(max_length=200)
	location = models.CharField(max_length=200)
	latitude = models.FloatField()
	longitude = models.FloatField()
	timestamp = models.DateTimeField()
	photoURL = models.CharField(max_length=200)
	objectID = models.CharField(max_length=200)
	params = PickledObjectField()

	def __unicode__(self):
		return 'Description: ' + self.description + '\n' + 'ObjectID: ' + self.objectID

class DHUserProfile(models.Model):
	user = models.OneToOneField(User)
	parseToken = models.CharField(max_length=200)
