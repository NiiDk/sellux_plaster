from django.contrib import admin
from .models import City, ShippingSetting

@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ('name', 'base_delivery_fee')
    search_fields = ('name',)

@admin.register(ShippingSetting)
class ShippingSettingAdmin(admin.ModelAdmin):
    list_display = ('tax_rate', 'delivery_fee_per_100')
