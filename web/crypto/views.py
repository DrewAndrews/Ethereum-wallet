from django.shortcuts import render
from django.views.generic import TemplateView
from django.views.generic.edit import FormView
from .forms import TokenForm
from django.urls import reverse_lazy


class HomePageView(TemplateView):
    template_name = 'home.html'

class TransactionsPageView(TemplateView):
    template_name = "transactions.html"

class TokenFormView(FormView):
    form_class = TokenForm
    template_name = "new_token.html"
    success_url = reverse_lazy('Transactions')
