from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=120)
    description = models.TextField(blank=True)

    class Meta:
        verbose_name_plural = 'Categories'
        ordering = ['name']

    def __str__(self):
        return self.name


class MenuItem(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='items')
    name = models.CharField(max_length=140)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    is_available = models.BooleanField(default=True)
    preparation_time = models.PositiveIntegerField(default=15, help_text='in minutes')
    image = models.ImageField(upload_to='menu_items/', blank=True, null=True)
    customizations = models.JSONField(default=dict, blank=True, help_text='e.g., {"spice_level": ["mild", "medium", "hot"]}')

    class Meta:
        ordering = ['category', 'name']

    def __str__(self):
        return f"{self.name} ({self.category})"
