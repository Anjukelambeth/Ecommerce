
from django.urls import path
from . import views


urlpatterns = [

    path('refferalcode_apply/',views.refferalcode_apply,name='refferalcode_apply'),
    path('verify_refferalcode/',views.verify_refferalcode,name='verify_refferalcode'),

]
