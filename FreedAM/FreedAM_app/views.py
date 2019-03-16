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
import win32gui
import win32process
import pythoncom
import PIL.ImageGrab
from PIL import Image
import pywinauto
import re
import win32con

# Create your views here.


def home(request):
	# load homepage html template
	template = loader.get_template('FreedAM_app/templates/FreedAM_app/homepage.html')

	# contact_form = ContactForm(request.POST or None)
	# if contact_form.is_valid():
	# 	contact_form.save()
	context = {
	  # 'contact_form': contact_form,
	}
	return HttpResponse(template.render(context, request))	

def projects(request):
	# load projects page 
	template = loader.get_template('FreedAM_app/templates/FreedAM_app/projects.html')
	context = {
	   # 'latest_question_list': latest_question_list,
	}
	return HttpResponse(template.render(context, request))	

def calculator_home(request):
	# load calculator html page 
	template = loader.get_template('FreedAM_app/templates/FreedAM_app/calculator_home.html')
	# load input form 
	frame_input_form = FrameDimensionsForm(request.POST or None)

	#initialize pythoncom to allow connection to Inventor
	pythoncom.CoInitialize()	
	# Open Inventor
	invApp = win32com.client.Dispatch("Inventor.Application")

	# Make inventor visible
	invApp.Visible = True

	# Operate Inventor in the background
	invApp.SilentOperation = True

	# Set location of assembly
	Assembly_name = 'C:/Users/asidawi/Desktop/CAD_testing/Frame_assembly - Working_on_constraints.iam'

	# Open the model
	oDoc = invApp.Documents.Open(Assembly_name)

	# if the form is valid i.e. has no clear input errors
	if frame_input_form.is_valid():
		
		# get latest object created id - THIS IS NOT ROBUST!!!!!!!!!!!!!!!!!!!!!!!!
		object_created_id = FrameDimensions.objects.order_by('-pub_date')[0].id
		
		if frame_input_form.cleaned_data['angle_lower_leg_upper_leg'] > 105 or frame_input_form.cleaned_data['angle_lower_leg_upper_leg'] < 85:
			form_errors = "Please ensure that angles are greater than 85 or less than 105 degrees"
			context = {'form_errors': form_errors, 'frame_input_form': frame_input_form}
			return HttpResponse(template.render(context, request))	
		if frame_input_form.cleaned_data['seat_depth'] > 500 or frame_input_form.cleaned_data['seat_depth'] < 400:
			form_errors = "Please ensure that seat depth is between 400 and 500mm"
			context = {'form_errors': form_errors, 'frame_input_form': frame_input_form}
			return HttpResponse(template.render(context, request))	
		if frame_input_form.cleaned_data['seat_width'] > 600 or frame_input_form.cleaned_data['seat_depth'] < 400:
			form_errors = "Please ensure that seat width is between 400 and 600mm"
			context = {'form_errors': form_errors, 'frame_input_form': frame_input_form}
			return HttpResponse(template.render(context, request))	
		if frame_input_form.cleaned_data['seat_height'] > 500 or frame_input_form.cleaned_data['seat_depth'] < 400:
			form_errors = "Please ensure that seat depth is between 400 and 500mm"
			context = {'form_errors': form_errors, 'frame_input_form': frame_input_form}
			return HttpResponse(template.render(context, request))	
		if frame_input_form.cleaned_data['shoulder_height'] < frame_input_form.cleaned_data['seat_height'] or frame_input_form.cleaned_data['shoulder_height'] >1500:
			form_errors = "Please ensure that shoulder height is greater than seat height, and less than 1500mm"
			context = {'form_errors': form_errors, 'frame_input_form': frame_input_form}
			return HttpResponse(template.render(context, request))													
		
		# load spreadsheet with parameters stored
		os.chdir("C:/Users/asidawi/Desktop/CAD_testing")	
		wb = load_workbook('Parameters.xlsx')
		ws = wb['Sheet1']
		
		# assign spreadsheet values according to input data
		ws['B2'] = frame_input_form.cleaned_data['angle_lower_leg_upper_leg']
		ws['B3'] = frame_input_form.cleaned_data['seating_angle']
		ws['B4'] = frame_input_form.cleaned_data['backrest_angle']
		ws['B5'] = frame_input_form.cleaned_data['shoulder_height'] - frame_input_form.cleaned_data['seat_height']
		ws['B6'] = frame_input_form.cleaned_data['seat_depth']

		# calculate whether vertical tubes need to be extended 
		seat_height = frame_input_form.cleaned_data['seat_height']
		vertical_tube_length_rear = seat_height - 300
		vertical_tube_length_front = seat_height - 300
		seat_angle = frame_input_form.cleaned_data['seating_angle']
		distance_between_rear_joints_and_front_joints = frame_input_form.cleaned_data['seat_depth'] + 0.1*frame_input_form.cleaned_data['seat_depth'] - 40 + 25	
		
		# conditions for changing vertical tube angle and calculating the new length	
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

		# setting remainder spredsheet values from form inputs
		ws['B7'] = vertical_tube_length_front
		ws['B8'] = vertical_tube_length_rear
		ws['B9'] = frame_input_form.cleaned_data['seat_depth']		
		ws['B10'] = frame_input_form.cleaned_data['seat_width']/2 - 25
		ws['B11'] = frame_input_form.cleaned_data['seat_width']/2 - 25
		ws['B14'] = frame_input_form.cleaned_data['seat_width']

		# save parameters spreadsheet
		wb.save('Parameters.xlsx')	


		# # iLogic GUID
		# iLogicAddinGuid = "{3BDD8D79-2179-4B11-8A5A-257B1C0263AC}"
		# # load iLogic add-in
		# iLogic_addin = invApp.ApplicationAddIns.ItemById(iLogicAddinGuid)
		# # Activate the add-in
		# iLogic_addin.Activate()

		# _iLogicAutomation = iLogic_addin.Automation()

		# Access the iLogic rules within the model
		#rules = iLogic_addin.Rules(invApp)

		# Update assembly
		oDoc.Update()
		# Save assembly
		oDoc.Save()

		# Save as STL (needs testing)
		# oDoc.SaveAs("joint_name.stl", True)

		os.chdir("C:/Users/asidawi/Documents/FreedAM/FreedAM/FreedAM_app/static/images")	

		def enumHandler(hwnd, lParam):
			if win32gui.IsWindowVisible(hwnd):
				if 'Inventor' in win32gui.GetWindowText(hwnd):
					# win32gui.MinimiseWindow(hwnd)
					# win32gui.MaximiseWindow(hwnd)
					win32gui.ShowWindow(hwnd, win32con.SW_MINIMIZE)				
					win32gui.ShowWindow(hwnd, win32con.SW_MAXIMIZE)
					#win32gui.SetForegroundWindow(hwnd)

		win32gui.EnumWindows(enumHandler, None)

		Right_view = invApp.CommandManager.ControlDefinitions.Item("AppRightViewCmd").Execute()
		# take screenshot and crop to wheelchair size
		im = PIL.ImageGrab.grab()   
		im.crop((500, 150, 1500, 980)).save("FreedAM_"+str(object_created_id)+"_right.jpg")

		Front_view = invApp.CommandManager.ControlDefinitions.Item("AppFrontViewCmd").Execute()
		# take screenshot and crop to wheelchair size
		im = PIL.ImageGrab.grab()     
		im.crop((500, 150, 1500, 980)).save("FreedAM_"+str(object_created_id)+"_front.jpg")

		# Iso_view = invApp.CommandManager.ControlDefinitions.Item("AppIsometricViewCmd").Execute()

		win32gui.ShowWindow(7346022, win32con.SW_MINIMIZE)				

		# save frame input form data to database
		frame_input_form.save()

		# create an accessories object for the next page linked to the new frame
		new_accessories_object = Accessories(pub_date = datetime.datetime.now(), linked_frame = FrameDimensions.objects.get(id =object_created_id))
		new_accessories_object.save()

# use standard upholstery sizes and compared seat width and length to that (6 standard sizes)
# 400x400, 400x450, 400x500, 450x550, 450x600

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




 # WHAT HAPPENS NEXT? Cushioning and accessory options with preview of chair?

def frame_preview(request, id=None):
	template = loader.get_template('FreedAM_app/templates/FreedAM_app/frame_preview.html')
	# load measurements
	measurements = FrameDimensions.objects.get(id=id)
	front_image_location = '/static/images/FreedAM_'+str(id)+'_front.jpg'
	right_image_location = '/static/images/FreedAM_'+str(id)+'_right.jpg'

	accessories_form = AccessoriesForm(request.POST or None, instance = measurements)
	if accessories_form.is_valid():
		accessories_form.linked_frame = measurements
		accessories_form.save()

	# load preview image
	context = {
	   'frame_input_form': measurements, 'front_image_location': front_image_location, 'right_image_location': right_image_location, 'accessories_form': accessories_form
	}
	return HttpResponse(template.render(context, request))	
	#return render(request, "buildpage/add_note.html", context)

def FreedAM_project(request):
	template = loader.get_template('FreedAM_app/templates/FreedAM_app/FreedAM_project.html')

	context = {
	  # 'contact_form': contact_form,
	}
	return HttpResponse(template.render(context, request))	