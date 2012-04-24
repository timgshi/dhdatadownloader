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
	description = models.CharField(max_length=200, blank=True, null=True)
	level = models.IntegerField(blank=True, null=True)
	userID = models.CharField(max_length=200, blank=True, null=True)
	location = models.CharField(max_length=200, blank=True, null=True)
	latitude = models.FloatField(blank=True, null=True)
	longitude = models.FloatField(blank=True, null=True)
	timestamp = models.DateTimeField(blank=True, null=True)
	photoURL = models.CharField(max_length=200, blank=True, null=True)
	objectID = models.CharField(max_length=200)
	createdAt = models.DateTimeField(blank=True, null=True)
	params = PickledObjectField()

	def __unicode__(self):
		return 'Description: ' + self.description + '\n' + 'ObjectID: ' + self.objectID

class DHUserProfile(models.Model):
	user = models.OneToOneField(User)
	parseToken = models.CharField(max_length=200)
