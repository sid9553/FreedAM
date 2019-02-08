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

	angle_lower_leg_upper_leg = models.IntegerField(validators=[MinValueValidator(1)])
	backrest_angle = models.IntegerField(validators=[MinValueValidator(1)])	
	seating_angle = models.IntegerField(validators=[MinValueValidator(1)])	
	seat_width = models.IntegerField(validators=[MinValueValidator(1)])
	# enter as number then recommmend small,med,large
	seat_depth = models.IntegerField(validators=[MinValueValidator(1)])
	seat_height = models.IntegerField(validators=[MinValueValidator(1)])
	# seat height has to have max of 600mm
	backrest_height = models.IntegerField(validators=[MinValueValidator(1)])
	# 

	# centre_of_gravity (angle of main wheel to back support)
	# armrest boolean
	# back wheel boolean


	# 
	class Meta:
		verbose_name ="Frame dimensions"
	def __unicode__ (self):
			return self.pub_date			

	# hip_circumference = models.IntegerField(validators=[MinValueValidator(1)])
	# thigh_circumference = models.IntegerField(validators=[MinValueValidator(1)])
