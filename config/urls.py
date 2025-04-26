from django.contrib import admin
from django.urls import path,include
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('clients/', include('clients.urls')),
    path('projects/', include('projects.urls')),
    path('tasks/', include('tasks.urls')),
    path('inventory/', include('inventory.urls')),
    path('invoices/', include('invoices.urls')),
    path('', include('dashboard.urls')),
    path('', include('users.urls')),
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('pos/', include('pos.urls')),
    path('expenses/', include('expenses.urls')),
]
