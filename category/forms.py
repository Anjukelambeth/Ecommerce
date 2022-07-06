# from tkinter import Widget
from django import forms
from .models import category

class CategoryForm(forms.ModelForm):

    class Meta:
        model = category
        fields = '__all__'
    
    def __init__(self,*args,**kwargs):
        super(CategoryForm,self).__init__(*args,**kwargs)
        self.fields['category_name'].widget.attrs['class']= 'form-control'
        self.fields['slug'].widget.attrs['class']= 'form-control'
        self.fields['description'].widget.attrs['class']= 'form-control'
        # self.fields['cat_images'].widget.attrs['class']= 'form-control'
        
        # for field in self.fields:
        #     self.fields[field].widget.attrs['class']= 'form-control'
