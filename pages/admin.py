from django.contrib import admin
from .models import StaticPage, Testimonial

@admin.register(StaticPage)
class StaticPageAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'updated_at')
    prepopulated_fields = {'slug': ('title',)}

@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ('client_name', 'client_title', 'rating', 'is_featured')
    list_filter = ('is_featured', 'rating')
    search_fields = ('client_name', 'content')
