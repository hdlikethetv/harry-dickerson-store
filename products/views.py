from django.shortcuts import render, get_object_or_404
from .models import Product

def home(request):
    """
    Home page view - shows a selection of featured products
    """
    # Fetch 4 most recent products to feature on home page
    featured_products = Product.objects.all()[:4]
    
    context = {
        'brand_name': 'Harry Dickerson',
        'tagline': 'Androgynous Workwear',
        'featured_products': featured_products
    }
    return render(request, 'products/home.html', context)


def product_list(request):
    """
    Catalog page - shows all products
    """
    products = Product.objects.all()
    
    context = {
        'products': products
    }
    return render(request, 'products/product_list.html', context)


def product_detail(request, pk):
    """
    Individual product page
    pk = primary key (unique ID Django assigns every database record)
    get_object_or_404 = returns the product OR a 404 page if not found
    """
    product = get_object_or_404(Product, pk=pk)
    
    context = {
        'product': product
    }
    return render(request, 'products/product_detail.html', context)