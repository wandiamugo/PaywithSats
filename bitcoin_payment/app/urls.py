from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('verify/', views.verify, name='verify'),
    # path('content/<int:content_id>/pay/', views.pay_for_service, name='pay_for_content'),
    # path('payment/<payment_hash>/status/', views.payment_status, name='payment_status'),
    path('wallet-balance/', views.wallet_balance_view, name='wallet_balance'),
    path('generate-address/', views.generate_address_view, name='generate_address'),
    path('get_transactions/', views.get_transactions_view, name='gettransactions'),
]