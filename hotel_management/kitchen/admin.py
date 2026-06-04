from django.contrib import admin

from .models import KitchenOrderTicket


@admin.register(KitchenOrderTicket)
class KitchenOrderTicketAdmin(admin.ModelAdmin):
    list_display = ['id', 'order', 'status_display', 'created_at', 'started_at', 'completed_at']
    list_filter = ['created_at', 'started_at', 'completed_at']
    search_fields = ['order__id', 'order__table__number']
    readonly_fields = ['created_at', 'started_at', 'completed_at']
    ordering = ['-created_at']

    def status_display(self, obj):
        return obj.order.get_status_display()
    status_display.short_description = 'Order Status'
