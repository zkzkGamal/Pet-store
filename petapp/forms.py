from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import  Profile


class RegForm(UserCreationForm):
    
	class Meta:
		model = User
		fields = ['username', 'email', 'password1', 'password2']

class ProductSearchForm(forms.Form):
    product_name = forms.CharField(max_length=100, required=False)
