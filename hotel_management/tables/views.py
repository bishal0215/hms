from django.db.models import Prefetch
from django.shortcuts import get_object_or_404, redirect, render

from .forms import FloorForm, TableForm
from .models import Floor, Table


def table_dashboard(request):
    floors = Floor.objects.prefetch_related(
        Prefetch('tables', queryset=Table.objects.order_by('number'))
    ).order_by('level', 'name')
    table_form = TableForm(request.POST or None)

    if request.method == 'POST' and request.POST.get('form_type') == 'table' and table_form.is_valid():
        table_form.save()
        return redirect('table_dashboard')

    return render(request, 'tables/table_dashboard.html', {
        'floors': floors,
        'table_form': table_form,
    })


def floor_dashboard(request):
    floors = Floor.objects.order_by('level', 'name')
    floor_form = FloorForm(request.POST or None)

    if request.method == 'POST' and floor_form.is_valid():
        floor_form.save()
        return redirect('floor_dashboard')

    return render(request, 'tables/floor_dashboard.html', {
        'floors': floors,
        'floor_form': floor_form,
    })


def toggle_table(request, pk):
    table = get_object_or_404(Table, pk=pk)

    if table.status == Table.STATUS_FREE:
        table.status = Table.STATUS_OCCUPIED
    elif table.status == Table.STATUS_OCCUPIED:
        table.status = Table.STATUS_RESERVED
    else:
        table.status = Table.STATUS_FREE

    table.save()
    return redirect('table_dashboard')
