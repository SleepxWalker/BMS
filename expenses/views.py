from django.shortcuts import render, redirect, get_object_or_404
from .models import Expense
from .forms import ExpenseForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from users.decorators import role_in_required

@login_required
@role_in_required(['admin', 'manager'])
def expense_list(request):
    expenses = Expense.objects.order_by('-date')
    return render(request, 'expenses/expense_list.html', {'expenses': expenses})

@login_required
@role_in_required(['admin', 'manager'])
def expense_create(request):
    if request.method == 'POST':
        form = ExpenseForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Expense created successfully.")
            return redirect('expense_list')
    else:
        form = ExpenseForm()
    return render(request, 'expenses/expense_form.html', {'form': form})

@login_required
@role_in_required(['admin', 'manager'])
def expense_edit(request, pk):
    expense = get_object_or_404(Expense, pk=pk)
    if request.method == 'POST':
        form = ExpenseForm(request.POST, instance=expense)
        if form.is_valid():
            form.save()
            messages.success(request, "Expense updated successfully.")
            return redirect('expense_list')
    else:
        form = ExpenseForm(instance=expense)
    return render(request, 'expenses/expense_form.html', {'form': form, 'edit_mode': True})

@login_required
@role_in_required(['admin'])
def expense_delete(request, pk):
    expense = get_object_or_404(Expense, pk=pk)
    if request.method == 'POST':
        expense.delete()
        messages.success(request, "Expense deleted successfully.")
        return redirect('expense_list')
    return render(request, 'expenses/expense_confirm_delete.html', {'expense': expense})

@login_required
@role_in_required(['admin', 'manager'])
def expense_detail(request, pk):
    expense = get_object_or_404(Expense, pk=pk)
    return render(request, 'expenses/expense_detail.html', {'expense': expense})