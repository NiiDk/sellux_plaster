from django.contrib import admin
from .models import TeamMember, Department

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    search_fields = ('name',)

@admin.register(TeamMember)
class TeamMemberAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'job_title', 'department', 'is_management', 'order_weight', 'is_active')
    list_filter = ('department', 'is_active', 'is_management')
    search_fields = ('first_name', 'last_name', 'job_title')
    autocomplete_fields = ('department',)
    fieldsets = (
        (None, {
            'fields': ('first_name', 'last_name', 'job_title', 'email')
        }),
        ('Role & Department', {
            'fields': ('department', 'bio', 'is_management')
        }),
        ('Professional Details', {
            'fields': ('specialization', 'qualifications', 'linkedin_url')
        }),
        ('Display & Status', {
            'fields': ('profile_image', 'order_weight', 'is_active')
        }),
    )
