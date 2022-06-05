

from . import views
from django.urls import path

urlpatterns = [
    path('',views.index,name='index'),
    path('signin/',views.signin,name='signin'),
    path('register/',views.register,name='register'),
    path('signout/',views.signout,name='signout'),
    path('verification/',views.verification,name='verification'),
    path('verification1/<int:id>',views.verification1,name='verification1'),
    path('account_view/',views.account_view,name='account_view'),
    path('user_profile/',views.user_profile,name='user_profile'),
    path('user_profile_edit/',views.user_profile_edit,name='user_profile_edit'),
    path('add_address/',views.add_address,name='add_address'),
    path('change_password/',views.change_password,name='change_password'),

]
