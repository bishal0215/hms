from django.contrib import admin

from .models import Invoice, Payment


@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ['id', 'order', 'total', 'issued_at']
    readonly_fields = ['issued_at']


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ['id', 'invoice', 'amount', 'method', 'paid_at']
    readonly_fields = ['paid_at']
