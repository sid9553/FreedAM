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
		help_texts = {
			'angle_lower_leg_upper_leg': _('<i>The angle of the footrest position to the seat when viewed from the side. Recommended angles are between 90 and 105 degrees.</i>'),		
			'backrest_angle': _('<i>The angle of the backrest to the seat. Recommended angles are between 90 and 105 degrees.</i>'),	
			'seating_angle': _('<i>The angle of the seat to vertical. Recommended angles are between 85 and 105 degrees.</i>'),		
			'seat_width': _('<i>Hip breadth is used to determine the width of the seat. Currently we can only accept measurements between 400 and 600mm.</i>'),		
			'seat_depth': _('<i>Buttock to knee length is used to determine seat depth. This measurement should be taken from the mid-buttock to the knee.</i>'),		
			'seat_height': _('<i>Desired seat height can be approximately determined by your knee to foot measurement. Recommended values are between 400 and 600mm.</i>'),		
			'shoulder_height': _('<i>The height of your shoulders when seated is used to approximate the maximum height/length of the backrest. This value is usually between 800 and 1200mm.</i>'),		
        }
		def __init__(self, *args, **kwargs):
			super(FrameDimensionsForm, self).__init__(*args, **kwargs)
			for field in self.fields.values():
				field.error_messages['required'] ='The field {fieldname} is required.'.format(fieldname=field.label)	

class AccessoriesForm(forms.ModelForm):
	class Meta:
		model = Accessories
		fields = '__all__'
		exclude = ['pub_date', 'linked_frame']		
		# widgets = {
		# 	'name': Textarea(attrs={'cols': 80, 'rows': 1}),
		# 	'email_address': Textarea(attrs={'cols': 80, 'rows': 1}),
		# 	'query': Textarea(attrs={'cols': 80, 'rows': 2}),
  #       }
		def __init__(self, *args, **kwargs):
			super(AccessoriesForm, self).__init__(*args, **kwargs)
			for field in self.fields.values():
				field.error_messages['required'] ='The field {fieldname} is required.'.format(fieldname=field.label)				