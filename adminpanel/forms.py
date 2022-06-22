from django import forms
from adminpanel.models import CategoryOffer, ProductOffer
from orders.models import Order
from dataclasses import fields


class OrderEditForm(forms.ModelForm):
    class Meta:
        model = Order
        fields= '__all__'

#to get a calendar for add and edit the offers
class DateTimeLocal(forms.DateTimeInput):
    input_type = 'datetime-local'
    color ='Red'

class ProductOfferForm(forms.ModelForm):
    class Meta:
        model = ProductOffer
        fields = '__all__'
        widgets = {
            'valid_from':DateTimeLocal(),
            'valid_to':DateTimeLocal(),
        }
        def __init__(self,*args,**kwargs):
            super(ProductOfferForm, self).__init__(*args, **kwargs)

class CategoryOfferForm(forms.ModelForm):
    class Meta:
        model = CategoryOffer
        fields = '__all__'
        widgets = {
            'valid_from': DateTimeLocal(),
            'valid_to': DateTimeLocal(),
        }
    
        def __init__(self,*args,**kwargs):
            super(CategoryOfferForm, self).__init__(*args, **kwargs)
            