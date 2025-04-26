from django.shortcuts import render, redirect, get_object_or_404
from .models import Client
from .forms import ClientForm
from clients import models
from django.contrib.auth.decorators import login_required
from users.decorators import  role_in_required
from django.contrib import messages
from django.db.models import Q
from projects.models import Project


@login_required()
@role_in_required(['admin','manager'])
def client_list(request):
    query = request.GET.get('q', '')
    clients = Client.objects.all()

    if query:
        clients = clients.filter(
            Q(business_name__icontains=query) |
            Q(contact_name__icontains=query)
        )

    return render(request, 'clients/client_list.html', {
        'clients': clients,
        'query': query,
    })


@login_required()
def client_detail(request, pk):
    client = get_object_or_404(Client, pk=pk)
    if request.user.role == 'employee':
        projects = client.project_set.filter(is_active=True, assigned_team=request.user)
    else:
        projects = client.project_set.filter(is_active=True)

    return render(request, 'clients/client_detail.html', {
        'client': client,
        'projects': projects,
    })

@login_required()
@role_in_required(['admin','manager'])
def client_create(request):
    if request.method == 'POST':
        form = ClientForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('client_list')
    else:
        form = ClientForm()
    return render(request, 'clients/client_form.html', {'form': form})


@login_required()
@role_in_required(['admin'])
def deactivate_client(request, pk):
    client = get_object_or_404(Client, pk=pk)
    client.is_active = False
    client.save()
    return redirect('client_list')


@login_required()
@role_in_required(['admin', 'manager'])
def client_edit(request, pk):
    client = get_object_or_404(Client, pk=pk)
    if request.method == 'POST':
        form = ClientForm(request.POST, instance=client)
        if form.is_valid():
            form.save()
            messages.success(request, "Client updated successfully.")
            return redirect('client_list')
    else:
        form = ClientForm(instance=client)
    return render(request, 'clients/client_form.html', {'form': form, 'edit_mode': True})


@login_required()
@role_in_required(['admin', 'manager'])
def client_delete(request, pk):
    client = get_object_or_404(Client, pk=pk)
    client.is_active = False  # מחיקה רכה
    client.save()
    messages.success(request, "Client deactivated successfully.")
    return redirect('client_list')