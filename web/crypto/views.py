from django.shortcuts import redirect, render
from .forms import TokenForm, UserForm

import sys

sys.path.append('../blockchain/')

from kyc import AccountManager


account = AccountManager()

def home_page(request):
    if account.is_logged_in():
        balance = account.get_balance()
        
        context = {
            'account': account,
            'balance': balance
        }
        
        return render(request,'home.html', context)
    else:
        return signup_page(request)
    
def transaction_page(request):
    if account.is_logged_in():
        payments = account.show_payments()
        
        context = {
            'payments': payments,
            'account': account
        }
        
        return render(request, 'transactions.html', context)
    else:
        return signup_page(request)
    
    
def signup_page(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            phone = form.cleaned_data['phone']
            password = form.cleaned_data['password']
            account.login(phone, password)
            balance = account.get_balance()
            
            context = {
                'account': account,
                'balance': balance
            }
            
            return render(request,'home.html', context)
    else:
        form = UserForm()
        
    return render(request, 'signup.html', {'form': form})
    

def send_token_page(request):
    if account.is_logged_in():
        
        context = {
                    'account': account
        }
        
        if request.method == 'POST':
            form = TokenForm(request.POST)
            if form.is_valid():
                address = form.cleaned_data['address']
                value = form.cleaned_data['value']
                account.make_transaction(address, value)
                return render(request, 'transactions.html', context)
            else:
                return signup_page(request)
        else:
            form = TokenForm()
        return render(request, 'new_token.html', {'form': form, 'account': account})
    return signup_page(request)

def log_out(request):
    print("1")
    account.logout()
    return signup_page(request)