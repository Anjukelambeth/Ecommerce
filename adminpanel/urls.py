

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
    path('cancel_order_admin/<int:order_number>',views.cancel_order_admin,name='cancel_order_admin'),
    path('return_order_admin/<int:order_number>',views.return_order_admin,name='return_order_admin'),
    path('order_order/<int:order_number>',views.order_order,name='order_order'),
    path('ship_order/<int:order_number>',views.ship_order,name='ship_order'),
    path('deliver_order/<int:order_number>',views.deliver_order,name='deliver_order'),
    path('order_cancel/<int:order_number>',views.order_cancel,name='order_cancel'), 
    path('admin_offerview',views.admin_offerview,name='admin_offerview'),
    path('add_product_offer',views.add_product_offer,name='add_product_offer'),
    path('edit_product_offer/<int:id>',views.edit_product_offer,name='edit_product_offer'),
    path('activate_product_offer',views.activate_product_offer, name = 'activate_product_offer'),     
    path('block_product_offer',views.block_product_offer, name = 'block_product_offer'),
    # path('delete_product_offer/<int:id>',views.delete_product_offer,name='delete_product_offer'),
    path('delete_product_offer',views.delete_product_offer, name = 'delete_product_offer'),
    path('export_csv',views.export_csv,name='export_csv'),
    path('export_excel',views.export_excel,name='export_excel'),
    # path('export_pdf',views.export_pdf,name='export_pdf'),
    path('report', views.report, name='report'),
    path('report_pdf', views.report_pdf, name='report_pdf'),
    path('sales_report', views.sales_report, name='sales_report'),
    path('add_coupon',views.add_coupon, name = 'add_coupon'),
    path('edit_coupon/<int:c_id>',views.edit_coupon, name = 'edit_coupon'),    
    path('activate_coupon',views.activate_coupon, name = 'activate_coupon'),     
    path('block_coupon',views.block_coupon, name = 'block_coupon'),
    path('delete_coupon',views.delete_coupon, name = 'delete_coupon'),
    # path('add_refferal',views.add_refferal, name = 'add_refferal'),
    # path('edit_refferal/<int:c_id>',views.edit_refferal, name = 'edit_refferal'),    
    # path('activate_refferal',views.activate_refferal, name = 'activate_refferal'),     
    # path('block_refferal',views.block_refferal, name = 'block_refferal'),
    # path('delete_refferal',views.delete_coupon, name = 'delete_refferal'),
    path('add_cat_offer',views.add_cat_offer, name = 'add_cat_offer'),
    path('edit_cat_offer/<int:cat_id>',views.edit_cat_offer, name="edit_cat_offer"),
    path('activate_cat_offer',views.activate_cat_offer, name = 'activate_cat_offer'),     
    path('block_cat_offer',views.block_cat_offer, name = 'block_cat_offer'),
    path('delete_cat_offer',views.delete_cat_offer, name = 'delete_cat_offer'),
    path('sales_report2/', views.sales_report2, name='sales_report2'),
    path('monthly_report/', views.monthly_report, name='monthly_report'),
    path('yearly_report/', views.yearly_report, name='yearly_report'),
    # path('weekly_report/<int:date>/', views.weekly_report, name='weekly_report'),
    path('add_prod_variation/',views.add_prod_variation, name = 'add_prod_variation'),
    path('admin_variation_table',views.admin_variation_table, name = 'admin_variation_table'),
    # path('admin_order2/',views.admin_order2,name='admin_order2'), 
]
