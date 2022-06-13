

from . import views
from django.urls import path

urlpatterns = [
    path('admin_panel/',views.admin_panel,name='admin_panel'),
    path('admin_home/',views.admin_home,name='admin_home'),
    path('admin_signout/',views.admin_signout,name='admin_signout'),
    path('admin_usersview/',views.admin_usersview,name='admin_usersview'),
    # path('userblock/',views.userblock,name='userblock'),  
    path('userunblock/<int:id>',views.userunblock,name='userunblock'),
    path('admin_userblock/<int:id>',views.admin_userblock,name='admin_userblock'),
    path('admin_category/',views.admin_category,name='admin_category'),
    path('edit_category/<int:id>',views.edit_category,name='edit_category'), 
    path('add_category/',views.add_category,name='add_category'),  
    path('delete_category/<int:id>',views.delete_category,name='delete_category'),
    path('admin_products/',views.admin_products,name='admin_products'), 
    path('add_products/',views.add_products,name='add_products'), 
    path('edit_products/<int:id>',views.edit_products,name='edit_products'), 
    path('delete_products/<int:id>',views.delete_products,name='delete_products'),
    path('admin_order/',views.admin_order,name='admin_order'), 
    path('admin_orderedit/<int:order_number>',views.admin_orderedit,name='admin_orderedit'), 
    path('order_cancel/<int:order_number>',views.order_cancel,name='order_cancel'), 
    path('admin_offerview',views.admin_offerview,name='admin_offerview'),
    path('add_product_offer',views.add_product_offer,name='add_product_offer'),
    path('edit_product_offer/<int:id>',views.edit_product_offer,name='edit_product_offer'),
    path('delete_product_offer/<int:id>',views.delete_product_offer,name='delete_product_offer'),

    

]
