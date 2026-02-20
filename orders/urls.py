from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    path('create/', views.order_create, name='order_create'),
    path('payment/<int:order_id>/', views.payment, name='payment'),
    path('payment/success/', views.payment_success, name='payment_success'),
    path('payment/cancelled/', views.payment_cancelled, name='payment_cancelled'),
    path('<int:order_id>/', views.order_detail, name='order_detail'),
    path('history/', views.order_history, name='order_history'),
]