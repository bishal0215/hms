from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from django.utils import timezone
from django.http import JsonResponse
from django.views.decorators.http import require_POST

from orders.models import Order
from .models import KitchenOrderTicket


def kot_dashboard(request):
    """Kitchen dashboard showing all pending and active orders."""
    pending_orders = Order.objects.filter(
        status__in=['pending', 'preparing']
    ).select_related('table', 'waiter').prefetch_related('items__menu_item').order_by('created_at')
    
    ready_orders = Order.objects.filter(
        status='ready'
    ).select_related('table').prefetch_related('items__menu_item').order_by('-updated_at')[:10]
    
    context = {
        'pending_orders': pending_orders,
        'ready_orders': ready_orders,
        'pending_count': pending_orders.count(),
    }
    return render(request, 'kitchen/dashboard.html', context)


def kitchen_fullscreen(request):
    """Full-screen kitchen view optimized for display screens."""
    pending_orders = Order.objects.filter(
        status__in=['pending', 'preparing']
    ).select_related('table', 'waiter').prefetch_related('items__menu_item').order_by('created_at')
    
    ready_orders = Order.objects.filter(
        status='ready'
    ).select_related('table').prefetch_related('items__menu_item').order_by('-updated_at')[:20]
    
    context = {
        'pending_orders': pending_orders,
        'ready_orders': ready_orders,
        'pending_count': pending_orders.count(),
    }
    return render(request, 'kitchen/fullscreen.html', context)


def kot_list(request):
    """List all pending kitchen orders."""
    orders = Order.objects.filter(
        status__in=['pending', 'preparing']
    ).select_related('table', 'waiter').prefetch_related('items__menu_item').order_by('created_at')
    
    return render(request, 'kitchen/kot_list.html', {
        'orders': orders,
    })


def order_detail(request, order_id):
    """View order details from kitchen perspective."""
    order = get_object_or_404(
        Order.objects.select_related('table', 'waiter').prefetch_related('items__menu_item'),
        pk=order_id
    )
    
    items = order.items.select_related('menu_item').all()
    
    return render(request, 'kitchen/order_detail.html', {
        'order': order,
        'items': items,
    })


@require_POST
def start_preparing(request, order_id):
    """Mark order as being prepared."""
    order = get_object_or_404(Order, pk=order_id)
    
    if order.status == 'pending':
        order.status = 'preparing'
        order.save()
        
        # Update KOT
        kot, created = KitchenOrderTicket.objects.get_or_create(order=order)
        if not kot.started_at:
            kot.started_at = timezone.now()
            kot.save()
        
        messages.success(request, f'Order #{order.id} marked as preparing')
    
    return redirect('kitchen_dashboard')


@require_POST
def mark_ready(request, order_id):
    """Mark order as ready for delivery."""
    order = get_object_or_404(Order, pk=order_id)
    
    if order.status in ['pending', 'preparing']:
        order.status = 'ready'
        order.save()
        
        # Update KOT
        kot, created = KitchenOrderTicket.objects.get_or_create(order=order)
        kot.completed_at = timezone.now()
        kot.save()
        
        messages.success(request, f'Order #{order.id} is ready for delivery')
    
    return redirect('kitchen_dashboard')


@require_POST
def mark_served(request, order_id):
    """Mark order as served (for waiter confirmation)."""
    order = get_object_or_404(Order, pk=order_id)
    
    if order.status in ['ready', 'preparing']:
        order.status = 'served'
        order.save()
        messages.success(request, f'Order #{order.id} marked as served')
    
    return redirect('kitchen_dashboard')


def api_order_status(request, order_id):
    """API endpoint to get order status (for real-time updates)."""
    order = get_object_or_404(Order, pk=order_id)
    
    return JsonResponse({
        'id': order.id,
        'table': order.table.number,
        'status': order.status,
        'total': float(order.total_price),
        'item_count': order.items.count(),
        'created_at': order.created_at.isoformat(),
        'updated_at': order.updated_at.isoformat(),
    })


def api_orders_list(request):
    """Return a JSON list of orders for kitchen polling.

    Accepts optional `status` query param: 'pending', 'preparing', 'ready', 'served'.
    If provided, only orders with that status are returned under `orders`.
    Default behavior returns `pending` and `ready` groups for dashboard use.
    """
    status = request.GET.get('status')

    def serialize(qs):
        out = []
        for o in qs:
            items = []
            for it in o.items.all():
                items.append({
                    'name': it.menu_item.name,
                    'quantity': it.quantity,
                })
            out.append({
                'id': o.id,
                'table': getattr(o.table, 'display_number', o.table.number),
                'status': o.status,
                'total': float(o.total_price),
                'created_at': o.created_at.isoformat(),
                'updated_at': o.updated_at.isoformat(),
                'items': items,
            })
        return out

    if status:
        allowed = ['pending', 'preparing', 'ready', 'served']
        if status not in allowed:
            return JsonResponse({'error': 'invalid status'}, status=400)
        qs = Order.objects.filter(status=status).select_related('table').prefetch_related('items__menu_item').order_by('created_at')
        return JsonResponse({
            'count': qs.count(),
            'orders': serialize(qs),
        })

    # default grouped response for dashboard
    pending = Order.objects.filter(status__in=['pending', 'preparing']).select_related('table').prefetch_related('items__menu_item').order_by('created_at')
    ready_qs = Order.objects.filter(status='ready').select_related('table').prefetch_related('items__menu_item').order_by('-updated_at')[:20]

    pending_list = serialize(pending)
    ready_list = serialize(ready_qs)

    return JsonResponse({
        'pending_count': pending.count(),
        'pending': pending_list,
        'ready_count': len(ready_list),
        'ready': ready_list,
    })
