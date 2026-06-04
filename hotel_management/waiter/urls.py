from django.urls import path

from . import views

urlpatterns = [
    path('', views.table_dashboard, name='table_dashboard'),
    path('toggle/<int:pk>/', views.toggle_table, name='toggle_table'),
]
