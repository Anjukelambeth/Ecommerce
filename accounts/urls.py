

from . import views
from django.urls import path

urlpatterns = [
    path('',views.index,name='index'),
    path('signin/',views.signin,name='signin'),
    path('register/',views.register,name='register'),
    path('signout/',views.signout,name='signout'),
    path('verification/',views.verification,name='verification'),
    path('verification1/',views.verification1,name='verification1'),
    # path('account_view/',views.account_view,name='account_view'),
    path('user_profile/',views.user_profile,name='user_profile'),
    path('user_profile_edit/',views.user_profile_edit,name='user_profile_edit'),
    path('add_address/',views.add_address,name='add_address'),
    path('change_password/',views.change_password,name='change_password'),
    path('my_order/',views.my_order,name='my_order'),
    path('order_view/<int:order_id>',views.order_view,name='order_view'),
    path('user_order_cancel/<int:order_number>',views.user_order_cancel,name='user_order_cancel'),
    path('return_order/<int:order_number>',views.return_order,name='return_order'),
]
