from django.urls import path
from . import views

# app_name helps Django differentiate URLs if you have multiple apps
app_name = 'products'

urlpatterns = [
    path('', views.home, name='home'),  # empty string = root URL
]