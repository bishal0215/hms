from django.shortcuts import render, redirect, get_object_or_404

from .forms import TableForm
from .models import Table


def table_dashboard(request):
    tables = Table.objects.order_by('number')
    form = TableForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('table_dashboard')

    return render(request, 'waiter/table_dashboard.html', {
        'tables': tables,
        'form': form,
    })


def toggle_table(request, pk):
    table = get_object_or_404(Table, pk=pk)
    table.is_occupied = not table.is_occupied
    table.save()
    return redirect('table_dashboard')
