from django.contrib import admin
from .models import Payment,OrderProduct,Order
# Register your models here.
class OrderAdmin(admin.ModelAdmin):
    list_display=('order_total','user',)

class PaymentAdmin(admin.ModelAdmin):
    list_display=('amount_paid','user','payment_method')

admin.site.register(Payment,PaymentAdmin)
admin.site.register(Order,OrderAdmin)
admin.site.register(OrderProduct)