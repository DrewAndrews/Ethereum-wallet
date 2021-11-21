from django.shortcuts import render
from django.views.generic import TemplateView
from django.views.generic.edit import FormView
from .forms import TokenForm, UserForm
from django.urls import reverse_lazy
import sys

sys.path.append('../blockchain/')

from kyc import AccountManager


account = AccountManager()

#def get_redirect_url

def home_page(request):
    context = {
        'account': account
    }
    return render(request,'home.html', context)
    
def transaction_page(request):
 #   if account.is_logged_in:
#      context
        return render(request, 'transactions.html')
    
def signup_page(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        
        context = {
            'account': account
        }
        
        if form.is_valid():
            phone = form.cleaned_data['phone']
            password = form.cleaned_data['password']
            account.login(phone, password)
            return render(request,'home.html', context)
    else:
        form = UserForm()
        
    return render(request, 'signup.html', {'form': form})
    

def send_token_page(request):
    if request.method == 'POST':
        form = TokenForm(request.POST)
        if form.is_valid():
            address = form.cleaned_data['address']
            value = form.cleaned_data['value']
            return render(request, 'transactions.html')
    else:
        form = TokenForm()
    
    return render(request, 'new_token.html', {'form': form})   
