from django.contrib import admin
from .models import Service

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'cost_per_sqm', 'is_active')
    list_editable = ('cost_per_sqm', 'is_active')
    search_fields = ('name',)
    list_filter = ('is_active',)
