import stripe
from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.contrib import messages
from cart.cart import Cart
from .models import Order, OrderItem
from .forms import OrderCreateForm

# Configure Stripe
stripe.api_key = settings.STRIPE_SECRET_KEY


@login_required
def order_create(request):
    """
    Display checkout form and create order.
    """
    cart = Cart(request)
    
    if len(cart) == 0:
        messages.warning(request, 'Your cart is empty.')
        return redirect('products:product_list')
    
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        
        if form.is_valid():
            # Create order but don't save to database yet
            order = form.save(commit=False)
            order.user = request.user
            order.total_amount = cart.get_total_price()
            order.save()
            
            # Create order items from cart
            for item in cart:
                OrderItem.objects.create(
                    order=order,
                    product=item['product'],
                    price=item['price'],
                    quantity=item['quantity']
                )
            
            # Clear the cart
            cart.clear()
            
            # Redirect to payment
            return redirect('orders:payment', order_id=order.id)
    else:
        # Pre-fill form with user data
        form = OrderCreateForm(initial={
            'first_name': request.user.first_name,
            'last_name': request.user.last_name,
            'email': request.user.email,
        })
    
    return render(request, 'orders/order_create.html', {
        'cart': cart,
        'form': form
    })


@login_required
def payment(request, order_id):
    """
    Create Stripe Checkout Session and redirect to payment.
    """
    order = get_object_or_404(Order, id=order_id, user=request.user)
    
    if order.status == 'paid':
        messages.info(request, 'This order has already been paid.')
        return redirect('orders:order_detail', order_id=order.id)
    
    # Create line items for Stripe
    line_items = []
    for item in order.items.all():
        line_items.append({
            'price_data': {
                'currency': 'gbp',
                'unit_amount': int(item.price * 100),  # Stripe uses cents/pence
                'product_data': {
                    'name': item.product.name,
                },
            },
            'quantity': item.quantity,
        })
    
    # Create Stripe Checkout Session
    try:
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=line_items,
            mode='payment',
            success_url=request.build_absolute_uri(
                reverse('orders:payment_success')
            ) + f'?session_id={{CHECKOUT_SESSION_ID}}',
            cancel_url=request.build_absolute_uri(
                reverse('orders:payment_cancelled')
            ),
            client_reference_id=order.id,
            metadata={'order_id': order.id}
        )
        
        # Save session ID to order
        order.stripe_checkout_session_id = checkout_session.id
        order.save()
        
        # Redirect to Stripe Checkout
        return redirect(checkout_session.url, code=303)
        
    except Exception as e:
        messages.error(request, f'Payment error: {str(e)}')
        return redirect('orders:order_detail', order_id=order.id)


@login_required
def payment_success(request):
    """
    Handle successful payment.
    """
    session_id = request.GET.get('session_id')
    
    if session_id:
        try:
            # Retrieve session from Stripe
            session = stripe.checkout.Session.retrieve(session_id)
            
            # Get the order
            order = get_object_or_404(Order, id=session.metadata['order_id'])
            
            # Update order status
            order.status = 'paid'
            order.save()
            
            messages.success(request, f'Payment successful! Order #{order.id} confirmed.')
            return redirect('orders:order_detail', order_id=order.id)
            
        except Exception as e:
            messages.error(request, f'Error processing payment confirmation: {str(e)}')
            return redirect('products:home')
    
    return redirect('products:home')


@login_required
def payment_cancelled(request):
    """
    Handle cancelled payment.
    """
    messages.warning(request, 'Payment was cancelled. Your order is still pending.')
    return redirect('cart:cart_detail')


@login_required
def order_detail(request, order_id):
    """
    Display order details.
    """
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'orders/order_detail.html', {'order': order})


@login_required
def order_history(request):
    """
    Display user's order history.
    """
    orders = request.user.orders.all()
    return render(request, 'orders/order_history.html', {'orders': orders})