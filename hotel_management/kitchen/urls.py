from django.urls import path

from . import views

urlpatterns = [
    path('', views.kot_dashboard, name='kitchen_dashboard'),
    path('fullscreen/', views.kitchen_fullscreen, name='kitchen_fullscreen'),
    path('orders/', views.kot_list, name='kitchen_orders'),
    path('order/<int:order_id>/', views.order_detail, name='kitchen_order_detail'),
    path('order/<int:order_id>/start/', views.start_preparing, name='start_preparing'),
    path('order/<int:order_id>/ready/', views.mark_ready, name='mark_ready'),
    path('order/<int:order_id>/served/', views.mark_served, name='mark_served'),
    path('api/order/<int:order_id>/status/', views.api_order_status, name='api_order_status'),
    path('api/orders/', views.api_orders_list, name='api_orders_list'),
]
