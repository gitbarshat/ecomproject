from django import forms
from .models import *
from django.contrib.auth.models import User

class CheckoutForm(forms.ModelForm):
    class Meta:
        model = Order 
        fields = ['ordered_by','shipping_address','email','contact_no']

class CustomerregistrationForm(forms.ModelForm):
    username = forms.CharField(widget = forms.TextInput())
    password = forms.CharField(widget = forms.PasswordInput())
    email = forms.CharField(widget = forms.EmailInput())
    class Meta:
        model = Customer
        fields = ['username','password','email','full_name','address']

    def clean_username(self):
        uname = self.cleaned_data.get('username')
        if User.objects.filter(username = uname).exists():
            raise forms.ValidationError('Customer with this name already exists')

        return uname

class CustomerloginForm(forms.Form):
    username = forms.CharField(widget = forms.TextInput())
    password = forms.CharField(widget = forms.PasswordInput())
    
    