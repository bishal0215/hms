from django import forms

from .models import Table


class TableForm(forms.ModelForm):
    class Meta:
        model = Table
        fields = ['number']
        widgets = {
            'number': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Table number'}),
        }
        labels = {
            'number': 'Table Number',
        }
