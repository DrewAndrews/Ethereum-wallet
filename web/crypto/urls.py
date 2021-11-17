from django.urls import path

from .views import HomePageView, TransactionsPageView, TokenFormView

urlpatterns = [
    path('', HomePageView.as_view(), name='Home'),
    path('transactions/', TransactionsPageView.as_view(), name='Transactions'), 
    path('transactions/new/', TokenFormView.as_view(), name='New_token'),
]
