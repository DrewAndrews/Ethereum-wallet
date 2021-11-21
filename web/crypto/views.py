from django.shortcuts import render
from django.views.generic import TemplateView
from django.views.generic.edit import FormView
from .forms import TokenForm, UserForm
from django.urls import reverse_lazy
import sys

sys.path.append('../blockchain/')

from kyc import AccountManager


account = AccountManager()


class HomePageView(TemplateView):
    template_name = 'home.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['account'] = account
        return context
    
    def get_redirect_url

class TransactionsPageView(TemplateView):
    template_name = "transactions.html"
    
class SignUpPageView(FormView):
    form_class = UserForm
    template_name = 'signup.html'
    success_url = reverse_lazy('Home')
    
    def form_valid(self, form):
        phone = form.cleaned_data['phone']
        password = form.cleaned_data['password']
        account.login(phone, password)
        return super().form_valid(form)
    

class TokenFormView(FormView):
    form_class = TokenForm
    template_name = "new_token.html"
    success_url = reverse_lazy('Transactions')
    
