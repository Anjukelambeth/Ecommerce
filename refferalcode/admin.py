from django.contrib import admin


from refferalcode.models import Refferal

# Register your models here.
class RefferalAdmin(admin.ModelAdmin):
    list_display = ['code','valid_from','valid_to','discount','active']
    list_filter = ['active','valid_from','valid_to']
    search_fields = ['code']

admin.site.register(Refferal,RefferalAdmin)