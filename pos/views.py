from django.shortcuts import render, redirect, get_object_or_404
from .models import Sale, SaleItem
from .forms import SaleForm, SaleItemForm
from inventory.models import Inventory
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from users.decorators import  role_in_required

@login_required()
def create_sale(request):
    if request.method == 'POST':
        sale_form = SaleForm(request.POST)
        item_form = SaleItemForm(request.POST)

        if sale_form.is_valid() and item_form.is_valid():
            sale = sale_form.save(commit=False)

            if not sale.client and sale_form.cleaned_data.get('manual_client_name'):
                sale.manual_client_name = sale_form.cleaned_data['manual_client_name']
            sale.save()

            item = item_form.cleaned_data['item']
            description = item_form.cleaned_data['description']
            quantity = item_form.cleaned_data['quantity']
            price = item_form.cleaned_data['price_at_time']

            if item:
                # ודא כמות זמינה
                if item.quantity < quantity:
                    messages.error(request, f"Not enough quantity in stock for {item.product_name}.")
                    return render(request, 'pos/sale_create.html', {
                        'sale_form': sale_form,
                        'item_form': item_form
                    })

                # משיכת פרטי פריט
                description = item.description
                price = item.price



            SaleItem.objects.create(
                sale=sale,
                item=item,
                description=description,
                quantity=quantity,
                price_at_time=price
            )

            sale.total_amount = quantity * price
            sale.save()

            return redirect('sale_detail', pk=sale.pk)

    else:
        sale_form = SaleForm()
        item_form = SaleItemForm()

    return render(request, 'pos/sale_create.html', {
        'sale_form': sale_form,
        'item_form': item_form
    })

@login_required()
def sale_detail(request, pk):
    sale = get_object_or_404(Sale, pk=pk)
    return render(request, 'pos/sale_detail.html', {'sale': sale})


@login_required()

def sale_list(request):
    sales = Sale.objects.select_related('client').order_by('-sale_date')
    return render(request, 'pos/sale_list.html', {'sales': sales})