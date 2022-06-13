from django.contrib import admin

from adminpanel.models import ProductOffer

# Register your models here.
class ProductOfferAdmin(admin.ModelAdmin):
    list_diplay=['product','active']
    list_filter = ['product']
admin.site.register(ProductOffer,ProductOfferAdmin)
