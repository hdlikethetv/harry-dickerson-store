from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from products.models import Product
from .cart import Cart


def cart_detail(request):
    """
    Display the shopping cart page.
    """
    cart = Cart(request)
    return render(request, 'cart/cart_detail.html', {'cart': cart})


@require_POST
def cart_add(request, product_id):
    """
    Add a product to the cart.
    This view only accepts POST requests for security.
    """
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    
    # Get quantity from the form, default to 1
    quantity = int(request.POST.get('quantity', 1))
    
    cart.add(product=product, quantity=quantity)
    
    return redirect('cart:cart_detail')


@require_POST
def cart_remove(request, product_id):
    """
    Remove a product from the cart.
    """
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    
    return redirect('cart:cart_detail')


@require_POST
def cart_update(request, product_id):
    """
    Update the quantity of a product in the cart.
    """
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    
    quantity = int(request.POST.get('quantity', 1))
    
    if quantity > 0:
        cart.add(product=product, quantity=quantity, override_quantity=True)
    else:
        cart.remove(product)
    
    return redirect('cart:cart_detail')