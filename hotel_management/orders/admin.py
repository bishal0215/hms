from django.contrib import admin

from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1
    fields = ['menu_item', 'quantity', 'special_instructions']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'table', 'waiter', 'status', 'total_price', 'created_at']
    list_filter = ['status', 'created_at', 'table__floor']
    search_fields = ['table__number', 'waiter__user__username']
    readonly_fields = ['total_price', 'created_at', 'updated_at']
    inlines = [OrderItemInline]
    fieldsets = (
        ('Order Info', {
            'fields': ('table', 'waiter', 'status')
        }),
        ('Pricing', {
            'fields': ('total_price',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def save_related(self, request, form, formsets, change):
        """Auto-calculate total after saving related items."""
        super().save_related(request, form, formsets, change)
        if form.instance:
            form.instance.calculate_total()


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['order', 'menu_item', 'quantity', 'get_subtotal']
    list_filter = ['order__status', 'menu_item__category']
    search_fields = ['order__id', 'menu_item__name']

    def get_subtotal(self, obj):
        return f"${obj.get_subtotal()}"
    get_subtotal.short_description = 'Subtotal'
