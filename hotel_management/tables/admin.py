from django.contrib import admin

from .models import Floor, Table


@admin.register(Floor)
class FloorAdmin(admin.ModelAdmin):
    list_display = ['name', 'level']
    ordering = ['level', 'name']


@admin.register(Table)
class TableAdmin(admin.ModelAdmin):
    list_display = ['display_number', 'floor', 'capacity', 'status']
    list_filter = ['floor', 'status']
    ordering = ['floor__level', 'number']

    def display_number(self, obj):
        return obj.display_number
    display_number.short_description = 'Table Number'
