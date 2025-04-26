from django.urls import path
from . import views

urlpatterns = [
    path('', views.inventory_list, name='inventory_list'),
    path('new/', views.inventory_create, name='inventory_create'),
    path('<int:pk>/', views.inventory_detail, name='inventory_detail'),
    path('<int:pk>/edit/', views.inventory_edit, name='inventory_edit'),
    path('<int:pk>/delete/', views.inventory_delete, name='inventory_delete'),
]