from django.db import models

from orders.models import Order


class KitchenOrderTicket(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name='kitchen_ticket')
    created_at = models.DateTimeField(auto_now_add=True)
    started_at = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"KOT #{self.id} - Order #{self.order.id} (Table {self.order.table.number})"

    def get_items_with_prep_time(self):
        """Return items grouped by preparation time."""
        items = self.order.items.select_related('menu_item').all()
        max_time = max(
            (item.menu_item.preparation_time for item in items),
            default=15
        )
        return items, max_time

    def is_overdue(self):
        """Check if order is taking longer than expected."""
        from django.utils import timezone
        if self.started_at:
            _, max_time = self.get_items_with_prep_time()
            elapsed = (timezone.now() - self.started_at).total_seconds() / 60
            return elapsed > max_time
        return False
