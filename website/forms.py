from django import forms
import datetime
from cheque.models import Receipt

categories = (
    ("Sport", "Sport"),
    ("Education", "Education")
)

currencies = (
    ("RUB", "RUB"),
    ("USD", "USD")
)


class SendReq(forms.ModelForm):
    category = forms.ChoiceField(choices=categories)
    amount = forms.FloatField()
    currency = forms.ChoiceField(choices=currencies)
    date = forms.DateField()
    file = forms.FileField()

    class Meta:
        model = Receipt
        fields = ['category', 'amount', 'currency', 'date', 'file', ]