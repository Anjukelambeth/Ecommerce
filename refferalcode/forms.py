from django import forms
from django.db.models import fields


from refferalcode.models import Refferal


class DateInput(forms.DateTimeInput):
    input_type = 'date'
    
class RefferalApplyForm(forms.ModelForm):
    class Meta:
        model = Refferal
        fields = ['code','valid_from','valid_to','discount','active']
        widgets = {
            'valid_from': DateInput(),
            'valid_to':DateInput(),
        }    
        def __init__(self,*args,**kwargs):
            super(RefferalApplyForm, self).__init__(*args, **kwargs)
           