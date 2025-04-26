from django.shortcuts import render, redirect, get_object_or_404
from .models import Inventory
from .forms import InventoryForm
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from users.decorators import  role_in_required
from django.contrib import messages


@login_required()

def inventory_list(request):
    query = request.GET.get('q', '')
    items = Inventory.objects.all()

    if query:
        items = items.filter(
            Q(product_name__icontains=query) |
            Q(category__icontains=query)
        )

    return render(request, 'inventory/inventory_list.html', {
        'items': items,
        'query': query,
    })

@login_required()
def inventory_detail(request, pk):
    item = get_object_or_404(Inventory, pk=pk)
    return render(request, 'inventory/inventory_detail.html', {'item': item})

@login_required()
@role_in_required(['admin','manager'])
def inventory_create(request):
    if request.method == 'POST':
        form = InventoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('inventory_list')
    else:
        form = InventoryForm()
    return render(request, 'inventory/inventory_form.html', {'form': form})


@login_required()
@role_in_required(['admin', 'manager'])
def inventory_edit(request, pk):
    item = get_object_or_404(Inventory, pk=pk)
    if request.method == 'POST':
        form = InventoryForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            messages.success(request, "Inventory item updated successfully.")
            return redirect('inventory_list')
    else:
        form = InventoryForm(instance=item)
    return render(request, 'inventory/inventory_form.html', {'form': form, 'edit_mode': True})

@login_required()
@role_in_required(['admin', 'manager'])
def inventory_delete(request, pk):
    item = get_object_or_404(Inventory, pk=pk)
    item.is_active = False  # מחיקה רכה
    item.save()
    messages.success(request, "Inventory item deactivated successfully.")
    return redirect('inventory_list')