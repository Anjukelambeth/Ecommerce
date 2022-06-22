from django.contrib import admin

from adminpanel.models import CategoryOffer, ProductOffer

# Register your models here.
class ProductOfferAdmin(admin.ModelAdmin):
    list_diplay=['product','active']
    list_filter = ['product']

class CategoryOfferAdmin(admin.ModelAdmin):
    list_display = ['category_id','valid_from','valid_to','discount','is_active']
    list_filter = ['is_active','valid_from','valid_to']
   

admin.site.register(CategoryOffer,CategoryOfferAdmin)
admin.site.register(ProductOffer,ProductOfferAdmin)
