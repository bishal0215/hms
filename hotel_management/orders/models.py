from django.db import models
from decimal import Decimal

from menu.models import MenuItem
from tables.models import Table
from users.models import UserProfile


class Order(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('preparing', 'Preparing'),
        ('ready', 'Ready'),
        ('served', 'Served'),
        ('cancelled', 'Cancelled'),
    )

    table = models.ForeignKey(Table, on_delete=models.CASCADE, related_name='orders')
    waiter = models.ForeignKey(UserProfile, on_delete=models.SET_NULL, null=True, blank=True, related_name='orders_taken')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Order #{self.id} - Table {self.table.number} ({self.status})"

    def calculate_total(self):
        """Calculate and update total price from order items."""
        total = sum(
            item.menu_item.price * item.quantity
            for item in self.items.all()
        )
        self.total_price = total
        self.save()
        return total

    def get_total(self):
        """Return current total price."""
        return self.total_price or self.calculate_total()


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    menu_item = models.ForeignKey(MenuItem, on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField(default=1)
    special_instructions = models.TextField(blank=True, help_text='e.g., no onions, extra spice')

    class Meta:
        ordering = ['id']

    def __str__(self):
        return f"{self.menu_item.name} x{self.quantity}"

    def get_subtotal(self):
        """Return subtotal for this item."""
        return self.menu_item.price * self.quantity
