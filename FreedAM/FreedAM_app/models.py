# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from django.core.validators import MinValueValidator
import datetime

# Contact.
class Contact(models.Model):
	pub_date = models.DateTimeField(default = datetime.datetime.now())
	name = models.CharField(max_length = 50)
	email_address = models.EmailField(max_length = 254)
	query = models.CharField(max_length = 250)
	class Meta:
		verbose_name ="Contact forms received"
	def __unicode__ (self):
			return self.name

# Frame dimensions.
class FrameDimensions(models.Model):
	pub_date = models.DateTimeField(default = datetime.datetime.now())

	angle_lower_leg_upper_leg = models.IntegerField()
	backrest_angle = models.IntegerField()	
	# should be between 90 and 105
	seating_angle = models.IntegerField()	
	# should be between 75 and 90
	seat_width = models.IntegerField(verbose_name = "Hip breadth")
	# enter as number then get closest standard size
	seat_depth = models.IntegerField(verbose_name = "Buttock to knee length")
	seat_height = models.IntegerField()
	# seat height has to have max of 600mm
	# backrest_height = models.IntegerField(validators=[MinValueValidator(1)])
	shoulder_height = models.IntegerField()
	# centre_of_gravity (angle of main wheel to back support)
	# back wheel boolean
	class Meta:
		verbose_name ="Frame dimensions"
	def __str__ (self):
			return self.pub_date			
