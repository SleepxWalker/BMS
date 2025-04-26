from django.shortcuts import render, redirect, get_object_or_404
from .models import Invoice, InvoiceItem
from .forms import InvoiceForm, InvoiceItemForm
from django.db.models import Q
from django.utils.dateparse import parse_date
from users.decorators import role_in_required
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.contrib import messages
from inventory.models import Inventory
from clients.models import Client


@login_required()
@role_in_required(['admin', 'manager'])
def invoice_list(request):
    query = request.GET.get('q', '')
    status_filter = request.GET.get('status', '')
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    min_total = request.GET.get('min_total')
    max_total = request.GET.get('max_total')

    invoices = Invoice.objects.select_related('client').all()

    if query:
        invoices = invoices.filter(client__business_name__icontains=query)

    if status_filter:
        invoices = invoices.filter(status=status_filter)

    if start_date:
        invoices = invoices.filter(issue_date__gte=parse_date(start_date))
    if end_date:
        invoices = invoices.filter(issue_date__lte=parse_date(end_date))

    if min_total:
        invoices = invoices.filter(total_amount__gte=min_total)
    if max_total:
        invoices = invoices.filter(total_amount__lte=max_total)

    return render(request, 'invoices/invoice_list.html', {
        'invoices': invoices,
        'query': query,
        'status_filter': status_filter,
        'start_date': start_date,
        'end_date': end_date,
        'min_total': min_total,
        'max_total': max_total,
    })


@login_required()
@role_in_required(['admin', 'manager'])
def invoice_create_with_item(request):
    if request.method == 'POST':
        invoice_form = InvoiceForm(request.POST)
        item_form = InvoiceItemForm(request.POST)

        manual_client_name = request.POST.get('manual_client', '').strip()

        if invoice_form.is_valid() and item_form.is_valid():
            invoice = invoice_form.save(commit=False)

            # שמירת שם לקוח ידני אם לא נבחר לקוח קיים
            if not invoice.client and manual_client_name:
                invoice.manual_client_name = manual_client_name
            elif invoice.client:
                invoice.manual_client_name = ''

            invoice.save()

            item = item_form.cleaned_data.get('item')
            description = item_form.cleaned_data.get('description')
            quantity = item_form.cleaned_data.get('quantity')
            price = item_form.cleaned_data.get('price')

            if item:
                if item.quantity < quantity:
                    messages.error(request, f"Not enough quantity for item {item.product_name}.")
                    return render(request, 'invoices/invoice_create_with_item.html', {
                        'invoice_form': invoice_form,
                        'item_form': item_form,
                    })

                description = item.description
                price = item.price

            InvoiceItem.objects.create(
                invoice=invoice,
                item=item,
                description=description,
                quantity=quantity,
                price_at_time=price
            )

            invoice.total_amount = quantity * price
            invoice.save()

            return redirect('invoice_detail', pk=invoice.pk)
        else:
            messages.error(request, "Form validation failed.")
    else:
        invoice_form = InvoiceForm()
        item_form = InvoiceItemForm()

    return render(request, 'invoices/invoice_create_with_item.html', {
        'invoice_form': invoice_form,
        'item_form': item_form,
    })


@login_required()
@role_in_required(['admin', 'manager'])
def invoice_detail(request, pk):
    invoice = get_object_or_404(Invoice, pk=pk)
    company_name = "My Business LTD"  # שנה לשם החברה שלך
    return render(request, 'invoices/invoice_detail.html', {
        'invoice': invoice,
        'company_name': company_name,
    })



@login_required()
@role_in_required(['admin', 'manager'])
def add_invoice_item(request, invoice_id):
    invoice = get_object_or_404(Invoice, id=invoice_id)
    if request.method == 'POST':
        form = InvoiceItemForm(request.POST)
        if form.is_valid():
            invoice_item = form.save(commit=False)
            invoice_item.invoice = invoice
            invoice_item.save()
            return redirect('invoice_detail', pk=invoice.id)
    else:
        form = InvoiceItemForm()
    return render(request, 'invoices/invoiceitem_form.html', {'form': form, 'invoice': invoice})


@login_required()
@role_in_required(['admin', 'manager'])
def invoice_edit(request, pk):
    invoice = get_object_or_404(Invoice, pk=pk)

    if invoice.status != 'Draft':
        messages.error(request, "Only draft invoices can be edited.")
        return redirect('invoice_list')

    if request.method == 'POST':
        form = InvoiceForm(request.POST, instance=invoice)
        if form.is_valid():
            form.save()
            messages.success(request, "Invoice updated successfully.")
            return redirect('invoice_list')
    else:
        form = InvoiceForm(instance=invoice)

    return render(request, 'invoices/invoice_form.html', {'form': form, 'edit_mode': True})

@login_required()
@role_in_required(['admin', 'manager'])
def invoice_delete(request, pk):
    invoice = get_object_or_404(Invoice, pk=pk)

    if invoice.status != 'Draft':
        messages.error(request, "Only draft invoices can be deleted.")
        return redirect('invoice_list')

    invoice.delete()
    messages.success(request, "Invoice deleted successfully.")
    return redirect('invoice_list')