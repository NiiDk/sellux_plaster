from django.contrib import admin
from .models import Project, ProjectImage

class ProjectImageInline(admin.TabularInline):
    model = ProjectImage
    extra = 3

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'completion_date', 'is_featured')
    search_fields = ('title', 'description')
    list_filter = ('is_featured', 'completion_date')
    prepopulated_fields = {'slug': ('title',)}
    inlines = [ProjectImageInline]
