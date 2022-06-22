
from . import views
from django.urls import path

urlpatterns = [
    path('',views.cart,name='cart'),
    path('add_cart/<str:product_id>',views.add_cart,name='add_cart'),
    path('remove_cart/<str:product_id>/<int:cart_item_id>/',views.remove_cart,name='remove_cart'),
    path('remove_items/',views.remove_items,name='remove_items'),
    path('checkout/',views.checkout,name='checkout'),
    path('add_cart_ajax/',views.add_cart_ajax,name='add_cart_ajax'),
    path('remove_cart_ajax/',views.remove_cart_ajax, name='remove_cart_ajax'),
    path('buyNow/<str:category_slug>/<str:product_slug>/',views.buyNow,name='buyNow'),
    
]
