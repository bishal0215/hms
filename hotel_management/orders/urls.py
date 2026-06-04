from django.urls import path

from . import views

urlpatterns = [
    path('', views.order_list, name='orders_index'),
    path('new/', views.create_order, name='create_order'),
    path('<int:pk>/', views.order_detail, name='order_detail'),
    path('<int:pk>/add-item/', views.add_item_to_order, name='add_item'),
    path('<int:order_pk>/item/<int:item_pk>/edit/', views.edit_item, name='edit_item'),
    path('<int:order_pk>/item/<int:item_pk>/remove/', views.remove_item_from_order, name='remove_item'),
    path('table/<int:table_pk>/', views.order_by_table, name='table_orders'),
]
