
from asyncio.windows_events import NULL
from dataclasses import fields
from pyexpat import model
from tkinter import Widget
from django.forms import ValidationError
from django import forms
from .models import Account,UserAddresses

class RegistrationForm(forms.ModelForm):
 
    password=forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder':'Enter your password',
        'class':'form-control'
    }))
    confirm_password =forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder':'Confirm password',
        'class':'form-control'
    }))
    class Meta:
        model  = Account
        fields = ['first_name','last_name','phone_number','email','password']

    def __init__(self,*args,**kwargs):
        super(RegistrationForm,self).__init__(*args,**kwargs)
        self.fields['first_name'].widget.attrs['placeholder']= 'Enter your first name'
        self.fields['last_name'].widget.attrs['placeholder']= 'Enter your last name'
        self.fields['email'].widget.attrs['placeholder']= 'Enter your email address'
        self.fields['phone_number'].widget.attrs['placeholder']= 'Enter your phone number'
        
        for field in self.fields:
            self.fields[field].widget.attrs['class']= 'form-control'

    def clean(self):
        cleaned_data = super(RegistrationForm, self).clean()
        password=cleaned_data.get('password')
        confirm_password =cleaned_data.get('confirm_password')
        if password!= confirm_password:
            raise forms.ValidationError(
                'password and confirm password does not match'
            )

class UserForm(forms.ModelForm):
    class Meta:
        model= Account
        fields=('first_name','last_name','email','phone_number')

    def __init__(self,*args,**kwargs):
        super(UserForm,self).__init__(*args,**kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class']= 'form-control'
            # self.fields[field].widget.attrs['class']= 'required '

class UserAddressForm(forms.ModelForm):
    class Meta:
        model= UserAddresses
        fields=('address_line_1','address_line_2','city','zipcode','state')
        widgets ={
            'address_line_1':forms.TextInput(attrs={'class':'form-control'}),
            'address_line_2':forms.TextInput(attrs={'class':'form-control'}),
            'city':forms.TextInput(attrs={'class':'form-control'}),
            'zipcode':forms.NumberInput(attrs={'class':'form-control'}),
            'state':forms.TextInput(attrs={'class':'form-control'}),

        }
    
    def __init__(self,*args,**kwargs):
        super(UserAddressForm,self).__init__(*args,**kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class']= 'form-control'
    
    def clean(self):
        cleaned_data = super(UserAddressForm, self).clean()