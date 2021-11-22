from django import forms


class CreateRequestForm(forms.Form):
    amount = forms.DecimalField(max_digits=10, label="Amount")
