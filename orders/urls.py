from django import views
from django.urls import path,include
from . import views
urlpatterns = [
    path('place_order/',views.place_order,name='place_order'),
    path('payments/',views.payments,name='payments'),
    path('cash_on_delivery<str:order_number>/',views.cash_on_delivery,name='cash_on_delivery'),
    path('paypal_complete/',views.paypal_complete,name='paypal_complete'),
    path('razor_success/',views.razor_success,name='razor_success'),
]