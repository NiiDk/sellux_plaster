from django.contrib import admin
from .models import AboutPage, CoreValue

class CoreValueInline(admin.TabularInline):
    model = CoreValue
    extra = 1

@admin.register(AboutPage)
class AboutPageAdmin(admin.ModelAdmin):
    inlines = [CoreValueInline]
