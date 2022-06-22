from django import forms
from django.db.models import fields

from coupons.models import Coupon


class DateInput(forms.DateTimeInput):
    input_type = 'date'
    
class CouponApplyForm(forms.ModelForm):
    class Meta:
        model = Coupon
        fields = ['code','valid_from','valid_to','discount','active']
        widgets = {
            'valid_from': DateInput(),
            'valid_to':DateInput(),
        }    
        def __init__(self,*args,**kwargs):
            super(CouponApplyForm, self).__init__(*args, **kwargs)
           