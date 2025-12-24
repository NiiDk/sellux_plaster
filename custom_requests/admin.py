from django.contrib import admin
from .models import CustomRequest

@admin.register(CustomRequest)
class CustomRequestAdmin(admin.ModelAdmin):
    list_display = ('project_title', 'user', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('project_title', 'user__username', 'description')
    list_editable = ('status',)
    readonly_fields = ('created_at',)
    fieldsets = (
        ('Request Info', {
            'fields': ('user', 'project_title', 'description', 'status')
        }),
        ('Images', {
            'fields': ('inspiration_image', 'site_photo')
        }),
        ('Admin Review', {
            'fields': ('admin_note', 'created_at')
        }),
    )
