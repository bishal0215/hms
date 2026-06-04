from django import forms

from .models import Order, OrderItem


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['table', 'waiter']
        widgets = {
            'table': forms.Select(attrs={'class': 'form-control'}),
            'waiter': forms.Select(attrs={'class': 'form-control'}),
        }
        labels = {
            'table': 'Select Table',
            'waiter': 'Assign Waiter (Optional)',
        }


class OrderItemForm(forms.ModelForm):
    class Meta:
        model = OrderItem
        fields = ['menu_item', 'quantity', 'special_instructions']
        widgets = {
            'menu_item': forms.Select(attrs={'class': 'form-control'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
            'special_instructions': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2,
                'placeholder': 'e.g., no onions, extra spice'
            }),
        }
        labels = {
            'menu_item': 'Menu Item',
            'quantity': 'Quantity',
            'special_instructions': 'Special Instructions',
        }


class OrderStatusForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['status']
        widgets = {
            'status': forms.Select(attrs={'class': 'form-control'}),
        }
        labels = {
            'status': 'Order Status',
        }
