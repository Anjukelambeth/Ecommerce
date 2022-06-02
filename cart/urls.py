
from . import views
from django.urls import path

urlpatterns = [
    path('',views.cart,name='cart'),
    path('add_cart/<str:product_id>',views.add_cart,name='add_cart'),
    path('remove_cart/<str:product_id>',views.remove_cart,name='remove_cart'),
    path('remove_items/<str:product_id>',views.remove_items,name='remove_items'),
    
]
