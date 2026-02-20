from django.contrib import admin
from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    """
    Allows editing OrderItems directly within the Order admin page.
    """
    model = OrderItem
    raw_id_fields = ['product']
    extra = 0


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'email', 'total_amount', 'status', 'created']
    list_filter = ['status', 'created']
    search_fields = ['id', 'email', 'first_name', 'last_name']
    inlines = [OrderItemInline]