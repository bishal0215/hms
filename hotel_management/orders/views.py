from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages

from menu.models import Category, MenuItem
from tables.models import Table
from users.models import UserProfile
from .forms import OrderForm, OrderItemForm, OrderStatusForm
from .models import Order, OrderItem


def order_list(request):
    """Display all orders, filterable by status."""
    orders = Order.objects.prefetch_related('items__menu_item').select_related('table', 'waiter')
    status = request.GET.get('status')
    if status:
        orders = orders.filter(status=status)
    return render(request, 'orders/order_list.html', {
        'orders': orders,
        'status_filter': status,
    })


def create_order(request):
    """Create a new order for a specific table."""
    form = OrderForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        order = form.save()
        messages.success(request, f'Order created for Table {order.table.number}')
        return redirect('order_detail', pk=order.pk)

    return render(request, 'orders/create_order.html', {
        'form': form,
    })


def order_detail(request, pk):
    """View and manage a specific order."""
    order = get_object_or_404(Order, pk=pk)
    items = order.items.select_related('menu_item').all()
    status_form = OrderStatusForm(request.POST or None, instance=order)

    if request.method == 'POST' and 'update_status' in request.POST:
        if status_form.is_valid():
            status_form.save()
            messages.success(request, 'Order status updated')
            return redirect('order_detail', pk=order.pk)

    return render(request, 'orders/order_detail.html', {
        'order': order,
        'items': items,
        'status_form': status_form,
    })


def add_item_to_order(request, pk):
    """Add an item to an existing order."""
    order = get_object_or_404(Order, pk=pk)
    
    # Only allow adding items if order is in pending or preparing status
    if order.status not in ['pending', 'preparing']:
        messages.error(request, 'Cannot add items to this order')
        return redirect('order_detail', pk=order.pk)

    form = OrderItemForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        item = form.save(commit=False)
        item.order = order
        item.save()
        order.calculate_total()
        messages.success(request, f'{item.menu_item.name} added to order')
        return redirect('order_detail', pk=order.pk)

    return render(request, 'orders/add_item.html', {
        'order': order,
        'form': form,
    })


def remove_item_from_order(request, order_pk, item_pk):
    """Remove an item from an order."""
    order = get_object_or_404(Order, pk=order_pk)
    item = get_object_or_404(OrderItem, pk=item_pk, order=order)

    if order.status not in ['pending', 'preparing']:
        messages.error(request, 'Cannot modify items in this order')
        return redirect('order_detail', pk=order.pk)

    item_name = item.menu_item.name
    item.delete()
    order.calculate_total()
    messages.success(request, f'{item_name} removed from order')
    return redirect('order_detail', pk=order.pk)


def edit_item(request, order_pk, item_pk):
    """Edit an item in an order."""
    order = get_object_or_404(Order, pk=order_pk)
    item = get_object_or_404(OrderItem, pk=item_pk, order=order)

    if order.status not in ['pending', 'preparing']:
        messages.error(request, 'Cannot modify items in this order')
        return redirect('order_detail', pk=order.pk)

    form = OrderItemForm(request.POST or None, instance=item)
    if request.method == 'POST' and form.is_valid():
        form.save()
        order.calculate_total()
        messages.success(request, 'Item updated')
        return redirect('order_detail', pk=order.pk)

    return render(request, 'orders/edit_item.html', {
        'order': order,
        'item': item,
        'form': form,
    })


def order_by_table(request, table_pk):
    """Show the menu and active orders for a specific table."""
    table = get_object_or_404(Table, pk=table_pk)
    categories = Category.objects.prefetch_related('items').all()
    order = table.orders.filter(status__in=['pending', 'preparing']).order_by('-created_at').first()
    orders = table.orders.filter(status__in=['pending', 'preparing', 'ready']).order_by('-created_at')

    if request.method == 'POST':
        menu_item_id = request.POST.get('menu_item_id')
        quantity = request.POST.get('quantity')
        special_instructions = request.POST.get('special_instructions', '').strip()

        if not menu_item_id:
            messages.error(request, 'Please select a menu item.')
            return redirect('table_orders', table_pk=table.pk)

        menu_item = get_object_or_404(MenuItem, pk=menu_item_id, is_available=True)
        quantity = int(quantity) if quantity and quantity.isdigit() else 1

        if not order:
            waiter = None
            if request.user.is_authenticated:
                waiter = getattr(request.user, 'userprofile', None)
            order = Order.objects.create(table=table, waiter=waiter)
            messages.success(request, f'Order #{order.id} created for Table {table.display_number}')

        OrderItem.objects.create(
            order=order,
            menu_item=menu_item,
            quantity=quantity,
            special_instructions=special_instructions,
        )
        order.calculate_total()
        messages.success(request, f'{menu_item.name} added to Order #{order.id}')
        return redirect('table_orders', table_pk=table.pk)

    return render(request, 'orders/table_orders.html', {
        'table': table,
        'order': order,
        'orders': orders,
        'categories': categories,
    })
