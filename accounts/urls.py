

from . import views
from django.urls import path

urlpatterns = [
    path('',views.index,name='index'),
    path('signin/',views.signin,name='signin'),
    path('register/',views.register,name='register'),
    path('signout/',views.signout,name='signout'),
    path('verification/',views.verification,name='verification'),
    path('verification1/<int:id>',views.verification1,name='verification1'),

]
