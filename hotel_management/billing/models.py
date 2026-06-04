from django.db import models

from orders.models import Order


class Invoice(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    issued_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Invoice #{self.id}"


class Payment(models.Model):
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, related_name='payments')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    paid_at = models.DateTimeField(auto_now_add=True)
    method = models.CharField(max_length=50)

    def __str__(self):
        return f"Payment #{self.id} ({self.method})"
