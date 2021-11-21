from django.urls import path

from .views import home_page, signup_page, transaction_page, send_token_page

urlpatterns = [
    path('', home_page, name='Home'),
    path('transactions/', transaction_page, name='Transactions'), 
    path('transactions/new/', send_token_page, name='New_token'),
    path('signup/', signup_page, name='Signup')
]
