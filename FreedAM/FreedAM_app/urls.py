from django.conf.urls import url
from django.contrib import admin
from FreedAM_app import views
from .models import *
from .views import *
urlpatterns = [
	url(r'^$', views.home, name='home'),
	url(r'^calculator_home/$', views.calculator_home, name='calculator_home'),
	url(r'^(?P<id>[\w-]+)/frame_preview/$', views.frame_preview, name='frame_preview'),
	#url(r'^partrequestinfo/$', views.partrequestinfo, name='partrequestinfo'),

]
