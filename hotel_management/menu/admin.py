from django.contrib import admin

from .models import Category, MenuItem


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'item_count']
    ordering = ['name']

    def item_count(self, obj):
        return obj.items.count()
    item_count.short_description = 'Items'


@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'price', 'is_available', 'preparation_time']
    list_filter = ['category', 'is_available']
    list_editable = ['is_available', 'price']
    search_fields = ['name', 'description']
    ordering = ['category', 'name']
    fieldsets = (
        ('Basic Info', {
            'fields': ('name', 'category', 'description', 'image')
        }),
        ('Pricing & Availability', {
            'fields': ('price', 'is_available', 'preparation_time')
        }),
        ('Customizations', {
            'fields': ('customizations',),
            'classes': ('collapse',)
        }),
    )
