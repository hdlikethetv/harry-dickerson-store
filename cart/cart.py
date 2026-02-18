from decimal import Decimal
from products.models import Product


class Cart:
    """
    A cart class that uses Django sessions to store cart items.
    """

    def __init__(self, request):
        """
        Initialize the cart.
        request = the HTTP request object that contains the session
        """
        self.session = request.session
        
        # Try to get existing cart from session
        cart = self.session.get('cart')
        
        # If no cart exists, create an empty one
        if not cart:
            cart = self.session['cart'] = {}
        
        self.cart = cart

    def add(self, product, quantity=1, override_quantity=False):
        """
        Add a product to the cart or update its quantity.
        
        product = Product object
        quantity = how many to add
        override_quantity = if True, replace quantity instead of adding to it
        """
        product_id = str(product.id)  # Session keys must be strings
        
        if product_id not in self.cart:
            # Product not in cart yet, add it
            self.cart[product_id] = {
                'quantity': 0,
                'price': str(product.price)  # Convert Decimal to string for JSON
            }
        
        if override_quantity:
            self.cart[product_id]['quantity'] = quantity
        else:
            self.cart[product_id]['quantity'] += quantity
        
        self.save()

    def save(self):
        """
        Mark the session as modified to make sure it gets saved.
        """
        self.session.modified = True

    def remove(self, product):
        """
        Remove a product from the cart.
        """
        product_id = str(product.id)
        
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def __iter__(self):
        """
        Loop through cart items and fetch the products from the database.
        This allows us to do: for item in cart
        """
        product_ids = self.cart.keys()
        
        # Get product objects from database
        products = Product.objects.filter(id__in=product_ids)
        
        cart = self.cart.copy()
        
        for product in products:
            # Add the product object to each cart item
            cart[str(product.id)]['product'] = product
        
        for item in cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item

    def __len__(self):
        """
        Count all items in the cart.
        This allows us to do: len(cart)
        """
        return sum(item['quantity'] for item in self.cart.values())

    def get_total_price(self):
        """
        Calculate total price of all items in cart.
        """
        return sum(Decimal(item['price']) * item['quantity'] 
                   for item in self.cart.values())

    def clear(self):
        """
        Remove cart from session.
        """
        del self.session['cart']
        self.save()