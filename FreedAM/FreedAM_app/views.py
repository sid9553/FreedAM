# -*- coding: utf-8 -*-
from django.shortcuts import render, get_object_or_404, redirect
from django import forms
from django.db import connections
from django.contrib import messages
from django.contrib.auth.models import *
from django.http import HttpResponse, Http404, HttpResponseRedirect, JsonResponse, HttpResponseServerError, StreamingHttpResponse
from django.template import RequestContext, loader
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.urlresolvers import reverse, reverse_lazy
from django.core.exceptions import ObjectDoesNotExist
from django.forms import formset_factory, BaseFormSet
from django.forms.models import  modelformset_factory, inlineformset_factory, model_to_dict
from django.views import generic
from django.db.models.signals import pre_save
from django.db.models import Sum, Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.serializers.json import DjangoJSONEncoder
from django.template.defaultfilters import filesizeformat
from django.utils import timezone
from datetime import datetime  
from django.utils.timezone import now, utc 
from django.core.mail import send_mail
from django.core import serializers
from django.core.files import File
from django.db import IntegrityError
from .forms import *
from openpyxl import load_workbook
import os
import win32com.client
import math
from win32com.client import constants
from win32com.client import gencache

# Create your views here.


def home(request):
	template = loader.get_template('FreedAM_app/templates/FreedAM_app/homepage.html')
	# contact_form = ContactForm(request.POST or None)
	# if contact_form.is_valid():
	# 	contact_form.save()
	context = {
	  # 'contact_form': contact_form,
	}
	return HttpResponse(template.render(context, request))	

def projects(request):
	template = loader.get_template('FreedAM_app/templates/FreedAM_app/projects.html')
	context = {
	   # 'latest_question_list': latest_question_list,
	}
	return HttpResponse(template.render(context, request))	

def calculator_home(request):
	template = loader.get_template('FreedAM_app/templates/FreedAM_app/calculator_home.html')
	frame_input_form = FrameDimensionsForm(request.POST or None)
	if frame_input_form.is_valid():
		print frame_input_form
		# save data
		
		print "hoogabooga"
		# get latest object created id - THIS IS NOT ROBUST!!!!!!!!!!!!!!!!!!!!!!!!
		object_created_id = FrameDimensions.objects.order_by('-pub_date')[0].id
		print object_created_id
		# update spreadsheet
		os.chdir("C:/Users/asidawi/Desktop/CAD_testing")	
		wb = load_workbook('Parameters.xlsx')
		ws = wb['Sheet1']
		ws['B2'] = frame_input_form.cleaned_data['angle_lower_leg_upper_leg']
		ws['B3'] = frame_input_form.cleaned_data['seating_angle']
		ws['B4'] = frame_input_form.cleaned_data['backrest_angle']
		ws['B5'] = frame_input_form.cleaned_data['shoulder_height'] - frame_input_form.cleaned_data['seat_height']
		ws['B6'] = frame_input_form.cleaned_data['seat_depth']
		# get seat height to determine initial length of vertical tubing		
		seat_height = frame_input_form.cleaned_data['seat_height']
		vertical_tube_length_rear = seat_height - 300
		vertical_tube_length_front = seat_height - 300
		seat_angle = frame_input_form.cleaned_data['seating_angle']
		distance_between_rear_joints_and_front_joints = frame_input_form.cleaned_data['seat_depth'] + 0.1*frame_input_form.cleaned_data['seat_depth'] - 40 + 25	
		# vertical tubes calculated from seat height and seat_angle	
		# use seat angle to determine how much needs to be added to vertical tubes
				
		if seat_angle > 90:
			angle_difference = seat_angle - 90
			additional_vertical_tube_length = math.tan(math.radians(angle_difference))*distance_between_rear_joints_and_front_joints
			vertical_tube_length_rear = vertical_tube_length_rear + additional_vertical_tube_length
		elif seat_angle < 90:
			angle_difference = 90 - seat_angle
			additional_vertical_tube_length = math.tan(math.radians(angle_difference))*distance_between_rear_joints_and_front_joints
			vertical_tube_length_front = vertical_tube_length_front + additional_vertical_tube_length
		else:
			pass
				
		ws['B7'] = vertical_tube_length_front
		ws['B8'] = vertical_tube_length_rear
		ws['B9'] = frame_input_form.cleaned_data['seat_depth']		
		ws['B10'] = frame_input_form.cleaned_data['seat_width']/2 - 10
		ws['B10'] = frame_input_form.cleaned_data['seat_width']/2 - 10
		ws['B14'] = frame_input_form.cleaned_data['seat_width']

		wb.save('Parameters.xlsx')	
		frame_input_form.save()	

		# update CAD

		# oApp = win32com.client.Dispatch('Inventor.Application')
		# oApp.Visible = True
		# mod = gencache.EnsureModule('{D98A091D-3A0F-4C3E-B36E-61F62068D488}', 0, 1, 0)
		# oApp = mod.Application(oApp)
		# oApp.SilentOperation = True
		# oDoc = oApp.ActiveDocument
		# prop = oApp.ActiveDocument.PropertySets.Item("Design Tracking Properties")

		# # getting description and designer from iproperties (works)
		# Descrip = prop('Description').Value
		# Designer = prop('Designer').Value
		# print(Descrip)
		# print(Designer)

		# oAssDoc = oApp.Documents.Open('someassemblyfile.iam')
		# ThisApplication.ActiveView.Update()
		# save it

		# take screenshot
		# import PIL.ImageGrab

		# im = PIL.ImageGrab.grab()     
		# im.show()  


		return redirect("FreedAM_app:frame_preview", object_created_id)
	else:
		form_errors = frame_input_form.errors
		print form_errors
		print "form invalid"
		context = {'form_errors': form_errors, 'frame_input_form': frame_input_form}
		return HttpResponse(template.render(context, request))		
	context = {
	   'frame_input_form': frame_input_form,
	}
	return HttpResponse(template.render(context, request))	


# use standard upholstery sizes and compared seat width and length to that (6 standard sizes)

# after frame created proceed to select cushioning and armrest options

 

def frame_preview(request, id=None):
	template = loader.get_template('FreedAM_app/templates/FreedAM_app/frame_preview.html')
	# load measurements
	measurements = FrameDimensions.objects.get(id=id)
	# load preview image
	context = {
	   'frame_input_form': measurements,
	}
	return HttpResponse(template.render(context, request))	
	#return render(request, "buildpage/add_note.html", context)
