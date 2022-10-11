from django import forms
from django.core.exceptions import ValidationError

from .models import Transactions, Accounts, TransactionsType
from transactions.fields import MoneyField


class TransactionForm(forms.ModelForm):
    money_value = MoneyField(widget=forms.TextInput(attrs={'class': 'form-control money_input'}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['accounts'].empty_label = "Счет транзакции не выбран"
        self.fields['transactions_type'].empty_label = "категория транзакции не выбрана"

    def clean(self):
        money_value = self.cleaned_data['money_value']
        transactions_type = self.cleaned_data['transactions_type']
        if money_value < 0 and transactions_type.main_type == True:
            raise ValidationError("В доходе не может быть отрицательное число")
        elif money_value > 0 and transactions_type.main_type == False:
            raise ValidationError("В расходе не может быть положительное число")
        elif money_value == 0:
            raise ValidationError("Я не буду сохранять транзакцию с нулём...")
        return self.cleaned_data

    class Meta:
        model = Transactions
        fields = ['money_value', 'comment', 'transactions_type', 'accounts']
        widgets = {
            # 'money_value': forms.TextInput(attrs={'class': 'form-control money_input'}),
            'comment': forms.TextInput(attrs={'class': 'form-control', 'rows': 5}),
            'transactions_type': forms.Select(attrs={'class': 'form-control money_input'}),
            'accounts': forms.Select(attrs={'class': 'form-control'})
        }


class AccountForm(forms.ModelForm):
    balans = MoneyField(widget=forms.TextInput(attrs={'class': 'form-control money_input'}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['accounts_type'].empty_label = "Тип не выбран"
        self.fields['currency'].empty_label = "Валюта не выбрана"

    class Meta:
        model = Accounts
        fields = ['title', 'balans', 'accounts_type', 'currency']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'rows': 5, 'verbose_name': "Красава молодец"}),
            'balans': forms.TextInput(attrs={'class': 'form-control money_input'}),
            'accounts_type': forms.Select(attrs={'class': 'form-control'}),
            'currency': forms.Select(attrs={'class': 'form-control'}),
        }


class TransactionTypeForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['currency'].empty_label = "Валюта категории не выбрана"

    class Meta:
        model = TransactionsType
        fields = ['category', 'currency', 'icons']
        widgets = {

            'main_type': forms.CheckboxInput(attrs={'class': 'main_type'}),
            'category': forms.TextInput(attrs={'class': 'form-control', 'type': 'text'}),
            'currency': forms.Select(attrs={'class': 'form-control'}),
            'icons': forms.Select(attrs={'class': 'form-control'})
        }
