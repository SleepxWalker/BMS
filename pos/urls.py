from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.create_sale, name='create_sale'),
    path('<int:pk>/', views.sale_detail, name='sale_detail'),
    path('', views.sale_list, name='sale_list'),
]