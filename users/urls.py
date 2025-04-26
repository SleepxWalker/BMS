from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('list/', views.user_list, name='user_list'),
    path('<int:pk>/', views.user_detail, name='user_detail'),
    path('edit/', views.user_edit, name='user_edit'),
    path('create/', views.user_create, name='user_create'),
    path('<int:pk>/edit-admin/', views.user_edit_admin, name='user_edit_admin'),
    path('<int:pk>/delete/', views.user_delete, name='user_delete'),


    path('change-password/', auth_views.PasswordChangeView.as_view(
        template_name='users/change_password.html',
        success_url='/users/password-changed/'
    ), name='change_password'),

    path('password-changed/', auth_views.PasswordChangeDoneView.as_view(
        template_name='users/password_changed.html'
    ), name='password_change_done'),
]
