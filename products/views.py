from django.shortcuts import render

def home(request):
    """
    This is our home page view.
    'request' contains info about the user's browser request.
    We're returning the rendered home.html template.
    """
    context = {
        'brand_name': 'Harry Dickerson',
        'tagline': 'Androgynous Workwear'
    }
    return render(request, 'products/home.html', context)