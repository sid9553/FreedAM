# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import *

# Register your models here.

class FrameDimensionsAdmin(admin.ModelAdmin):
	list_display = ["id", "pub_date"]
	# list_display_links = ["part_request_number"]
	# list_filter = ["requester", "partnumber", "pub_date", "project_id", "requestcancelled"]
	# search_fields = ["part_request_number", "partnumber", "customercontact", "project_manager", "project_id", "requester"]
	class Meta:
		model = FrameDimensions

admin.site.register(Contact)
admin.site.register(FrameDimensions, FrameDimensionsAdmin)