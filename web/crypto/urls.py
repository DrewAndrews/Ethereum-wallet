from django.urls import path

from .views import HomePageView, TokensPageView, TransactionsPageView

urlpatterns = [
    path('', HomePageView.as_view(), name='Home'),
    path('transactions/', TransactionsPageView.as_view(), name='Transactions'),
    path('tokens/', TokensPageView.as_view(), name='Tokens'), 
]
