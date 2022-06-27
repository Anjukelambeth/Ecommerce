from django import forms
from .models import Products, Variation

class ProductsForm(forms.ModelForm):

    class Meta:
        model = Products
        fields = '__all__'
    
    def __init__(self,*args,**kwargs):
        super(ProductsForm,self).__init__(*args,**kwargs)
        self.fields['product_name'].widget.attrs['class']= 'form-control'
        self.fields['slug'].widget.attrs['class']= 'form-control'
        self.fields['product_description'].widget.attrs['class']= 'form-control'
        # self.fields['cat_images'].widget.attrs['class']= 'form-control'
        self.fields['stock'].widget.attrs['class']= 'form-control'
        self.fields['is_available'].widget.attrs['class']= 'form-control'
        self.fields['category'].widget.attrs['class']= 'form-control'
        self.fields['category'].widget.attrs['class']= 'form-control'
        
        # for field in self.fields:
        #     self.fields[field].widget.attrs['class']= 'form-control'

class VariationForm(forms.ModelForm):

    class Meta:
        model = Variation
        fields = ['product','variation_category','variation_value','is_active']
