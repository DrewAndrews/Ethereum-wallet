from django import forms


class TokenForm(forms.Form):
    address = forms.CharField()
    value = forms.IntegerField()
