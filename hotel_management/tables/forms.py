from django import forms

from .models import Floor, Table


class FloorForm(forms.ModelForm):
    class Meta:
        model = Floor
        fields = ['name', 'level']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Floor name'}),
            'level': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Floor level'}),
        }
        labels = {
            'name': 'Floor Name',
            'level': 'Floor Level',
        }


class TableForm(forms.ModelForm):
    floor = forms.ModelChoiceField(
        queryset=Floor.objects.all(),
        empty_label='Select floor',
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='Floor',
    )

    class Meta:
        model = Table
        fields = ['floor', 'number', 'capacity', 'status']
        widgets = {
            'number': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Table number'}),
            'capacity': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Capacity'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
        }
        labels = {
            'number': 'Table Number',
            'capacity': 'Capacity',
            'status': 'Status',
        }
