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

	# os.chdir("C:/Users/asidawi/Documents/personal_development/FreedAM")	
	# wb = load_workbook('Parametric_joint_angle.xlsx')
	# ws = wb['Sheet1']
	# ws['B2'] = '30'
	# wb.save('Parametric_joint_angle.xlsx')	
	
	context = {
	   'frame_input_form': frame_input_form,
	}
	return HttpResponse(template.render(context, request))	

# use standard upholstery sizes and compared seat width and length to that
# change angle of certain joints depending on tube lengths

# after frame created proceed to select cushioning and armrest options

