from django.contrib import admin
from .models import Order, OrderItem

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['product']
    extra = 0

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'total_amount', 'status', 'payment_status', 'created_at')
    list_filter = ('status', 'payment_status', 'created_at')
    search_fields = ('user__username', 'email', 'paystack_ref')
    list_editable = ('status',)
    inlines = [OrderItemInline]
    
    fieldsets = (
        ('Order Info', {
            'fields': ('user', 'total_amount', 'status', 'payment_status', 'paystack_ref')
        }),
        ('Customer Details', {
            'fields': ('first_name', 'last_name', 'email', 'address', 'city')
        }),
        ('Admin Feedback', {
            'fields': ('admin_feedback',)
        }),
    )
