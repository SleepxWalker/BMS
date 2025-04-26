from django.urls import path
from . import views

urlpatterns = [
    path('', views.task_list, name='task_list'),
    path('new/', views.task_create, name='task_create'),
    path('<int:pk>/', views.task_detail, name='task_detail'),
    path('<int:task_id>/start/', views.start_timer, name='start_timer'),
    path('<int:task_id>/stop/', views.stop_timer, name='stop_timer'),
    path('<int:pk>/edit/', views.task_edit, name='task_edit'),
    path('<int:pk>/delete/', views.task_delete, name='task_delete'),
]