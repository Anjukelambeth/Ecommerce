from django import views
from django.urls import path,include
from . import views
urlpatterns = [
    path('place_order/',views.place_order,name='place_order'),
    path('payments/',views.payments,name='payments'),
    path('cash_on_delivery<str:order_number>/',views.cash_on_delivery,name='cash_on_delivery'),
    path('paypal_complete/',views.paypal_complete,name='paypal_complete'),
    path('razor_success/',views.razor_success,name='razor_success'),
    path('buy_place_order/<str:category_slug>/<str:product_slug>/',views.buy_place_order,name='buy_place_order'),
    path('buy_cash_on_delivery/<str:order_number>/<str:category_slug>/<str:product_slug>/',views.buy_cash_on_delivery,name='buy_cash_on_delivery'),
      path('buy_payments/<str:category_slug>/<str:product_slug>/',views.buy_payments,name='buy_payments'),

]