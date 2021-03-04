
from django.shortcuts import render, redirect
from .cart import Cart
from django.conf import settings
from django.contrib import messages
from .forms import CheckOutForm
from apps.order.utilities import checkout

def cart_detail(request):
    cart = Cart(request)
    
    if request.method == 'POST':
        form = CheckOutForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            phone = form.cleaned_data['phone']
            address = form.cleaned_data['address']
            zipcode = form.cleaned_data['zipcode']
            place = form.cleaned_data['place']
            
            order = checkout(request, first_name, last_name, email, address, zipcode, place, phone, cart.get_total_cost())
            cart.clear()
            
            return redirect('success')
    else:
        form = CheckOutForm()
            
            
    remove_from_cart = request.GET.get('remove_from_cart', '')
    change_quantity = request.GET.get('change_quantity', '')
    quantity = request.GET.get('quantity', 0)
    
    if remove_from_cart:
        
        cart.remove(remove_from_cart)
        return redirect('cart')
    
    if change_quantity:
        cart.add(change_quantity, quantity, True)
        return redirect('cart')
    
    return render(request, 'cart/cart.html', {'form': form,})

def success(request):
    return render(request,  'cart/success.html')