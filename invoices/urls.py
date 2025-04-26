from django.urls import path
from . import views

urlpatterns = [
    path('', views.invoice_list, name='invoice_list'),

    path('<int:pk>/', views.invoice_detail, name='invoice_detail'),
    path('<int:invoice_id>/add-item/', views.add_invoice_item, name='add_invoice_item'),
    path('new-with-item/', views.invoice_create_with_item, name='invoice_create_with_item'),
    path('<int:pk>/edit/', views.invoice_edit, name='invoice_edit'),
    path('<int:pk>/delete/', views.invoice_delete, name='invoice_delete'),
]