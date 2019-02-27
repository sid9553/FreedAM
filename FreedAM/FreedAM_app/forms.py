from django import forms
from django.forms import formset_factory, TimeInput, Textarea, NumberInput, TextInput, CheckboxInput, HiddenInput, SelectMultiple, Select
from django.forms.models import inlineformset_factory, modelformset_factory
from django.forms.extras.widgets import SelectDateWidget
from django.contrib.admin.widgets import AdminDateWidget 
from .models import *
from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import NON_FIELD_ERRORS, ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator

class ContactForm(forms.ModelForm):
	class Meta:
		model = Contact
		fields = '__all__'
		exclude = ['pub_date']		
		# widgets = {
		# 	'name': Textarea(attrs={'cols': 80, 'rows': 1}),
		# 	'email_address': Textarea(attrs={'cols': 80, 'rows': 1}),
		# 	'query': Textarea(attrs={'cols': 80, 'rows': 2}),
  #       }
		# help_texts = {
		# 	'name': _('<b>Start typing an address or company name to search database.'),		
		# 	'email_address': _('<b>Start typing a part number, description, or your DDM username to find your part. Tick this box to only show assemblies.'),		
		# 	'query': _('<b>This is the quantity of the above part number you would like to have built.<br> If you are unsure, please consult with manufacturing.<br>'),								
  #       }
		def __init__(self, *args, **kwargs):
			super(ContactForm, self).__init__(*args, **kwargs)
			for field in self.fields.values():
				field.error_messages['required'] ='The field {fieldname} is required.'.format(fieldname=field.label)	

class FrameDimensionsForm(forms.ModelForm):
	class Meta:
		model = FrameDimensions
		fields = '__all__'
		exclude = ['pub_date']		
		# widgets = {
		# 	'name': Textarea(attrs={'cols': 80, 'rows': 1}),
		# 	'email_address': Textarea(attrs={'cols': 80, 'rows': 1}),
		# 	'query': Textarea(attrs={'cols': 80, 'rows': 2}),
  #       }
		# help_texts = {
		# 	'name': _('<b>Start typing an address or company name to search database.'),		
		# 	'email_address': _('<b>Start typing a part number, description, or your DDM username to find your part. Tick this box to only show assemblies.'),		
		# 	'query': _('<b>This is the quantity of the above part number you would like to have built.<br> If you are unsure, please consult with manufacturing.<br>'),								
  #       }
		def __init__(self, *args, **kwargs):
			super(FrameDimensionsForm, self).__init__(*args, **kwargs)
			for field in self.fields.values():
				field.error_messages['required'] ='The field {fieldname} is required.'.format(fieldname=field.label)	