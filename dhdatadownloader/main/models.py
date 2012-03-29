from django.db import models

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

	def __unicode__(self):
		return 'Description: ' + self.description + '\n' + 'ObjectID: ' + self.objectID

# Create your models here.
