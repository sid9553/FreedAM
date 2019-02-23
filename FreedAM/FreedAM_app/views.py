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
from win32com.client import constants
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
		print "hoogabooga"
		print frame_input_form.pub_date
		os.chdir("C:/Users/asidawi/Desktop/personal_development/FreedAM")	
		wb = load_workbook('Parameters.xlsx')
		ws = wb['Sheet1']
		ws['B2'] = frame_input_form.angle_lower_leg_upper_leg
		ws['B3'] = frame_input_form.seating_angle	
		ws['B4'] = frame_input_form.backrest_angle
		ws['B5'] = frame_input_form.shoulder_height - frame_input_form.seat_height
		ws['B6'] = frame_input_form.seat_depth


		#ws['B8'] = frame_input_form.backrest_angle
		#ws['B8'] = frame_input_form.backrest_angle		
		# vertical tubes calculated from seat height and seat_angle

		ws['B9'] = frame_input_form.seat_depth		
		ws['B10'] = frame_input_form.seat_width/2 - 20
		ws['B10'] = frame_input_form.seat_width/2 - 20
		ws['B14'] = frame_input_form.seat_width


		wb.save('Parameters.xlsx')	
	
	context = {
	   'frame_input_form': frame_input_form,
	}
	return HttpResponse(template.render(context, request))	

# seat_depth = buttock to knee measurement + 25mm
# seat_width = hip breadth + 25mm


# use standard upholstery sizes and compared seat width and length to that (6 standard sizes)
# change angle of certain joints depending on tube lengths
# On changing seat angle, vertical tube sizes have to be updated as well as inner joint angles
# all calculations in python so minimal work done by inventor

# after frame created proceed to select cushioning and armrest options


#
# import win32com.client
# from win32com.client import gencache


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

