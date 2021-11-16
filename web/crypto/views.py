from django.shortcuts import render
from django.views.generic import TemplateView

class HomePageView(TemplateView):
    template_name = 'home.html'

class TokensPageView(TemplateView):
    template_name = "tokens.html"

class TransactionsPageView(TemplateView):
    template_name = "transactions.html"

