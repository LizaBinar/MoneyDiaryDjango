import os
from urllib.parse import urlencode

import openpyxl
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Sum
from django.http import QueryDict, HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DetailView

from transactions.forms import TransactionFrom, AccountForm, TransactionTypeForm
from transactions.models import Transactions, Accounts, TransactionsType, Icons

from transactions.make_exel import make_xlsx_file_in_response


def sum_balans(accounts):
    result = {}
    currents = accounts.order_by('currency').distinct().values('currency__title')
    for currency in currents:
        accounts_one_currency = accounts.filter(currency__title=currency['currency__title'])
        result[currency['currency__title']] = accounts_one_currency.aggregate(Sum("balans"))["balans__sum"]
    return result


def upload_exel(request):
    response = HttpResponse(content_type='exel/transactions_history')
    response['Content-Disposition'] = 'attachment; filename=transactions_history.xlsx'
    transactions = Transactions.objects.filter(owner=request.user)
    make_xlsx_file_in_response(response, transactions)
    return response





class MyTransactions(LoginRequiredMixin, ListView):
    model = Transactions
    template_name = "transactions/home_transactions_list.html"
    context_object_name = 'transactions'
    queryset = 'category'
    login_url = '/admin'

    # extra_context = {'title': 'Главная'}

    def get_context_data(self, *, object_list=None, **kwargs):
        accounts = Accounts.objects.filter(owner=self.request.user)
        context = super().get_context_data(**kwargs)
        context['title'] = 'Транзакции'
        context['transactions'] = Transactions.objects.filter(owner=self.request.user)
        context['accounts'] = accounts
        context['user'] = self.request.user
        context['sum_balans'] = QueryDict(urlencode(sum_balans(accounts)))
        return context


class TransactionDetail(LoginRequiredMixin, DetailView):
    model = Transactions  # pk=self.kwargs['category_id'])
    template_name = 'transactions/transactions_detail.html'
    # context_object_name = 'transaction'
    allow_empty = False

    def get_context_data(self, *, object_list=None, **kwargs):
        accounts = Accounts.objects.filter(owner=self.request.user)
        context = super().get_context_data(**kwargs)
        context['transactions'] = Transactions.objects.get(pk=self.kwargs['pk'])
        context['accounts'] = accounts
        return context

    #
    #
    # def get_context_data(self, *, object_list=None, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['transaction'] = Transactions.objects.get(pk=self.kwargs['transaction_id'])
    #     return context
    #
    # def get_queryset(self):
    #     return Transactions.objects.filter(pk=self.kwargs['transaction_id'])


# class TransactionsByCategory(LoginRequiredMixin, ListView):  # MyMixin
#     model = Transactions.objects.filter()
#     template_name = 'transactions/home_transactions_list.html'
#     context_object_name = 'transactions'
#     allow_empty = False
#     login_url = '/login/'
#
#     def get_context_data(self, *, object_list=None, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['title'] = TransactionsType.objects.get(pk=self.kwargs['transactions_type_id'])
#         context['accounts'] = Accounts.objects.filter(owner=self.request.user)
#         return context
#
#     def get_queryset(self):
#         return Transactions.objects.filter(transactions_type=self.kwargs['transactions_type_id'])


class AccountDetail(LoginRequiredMixin, DetailView):  # MyMixin
    model = Accounts
    template_name = "transactions/account_detail.html"
    allow_empty = False

    def get_context_data(self, *, object_list=None, **kwargs):
        accounts = Accounts.objects.filter(owner=self.request.user)
        context = super().get_context_data(**kwargs)
        context['account'] = Accounts.objects.get(pk=self.kwargs['pk'])
        context['accounts'] = accounts
        return context

    # def get_queryset(self):
    #     return Transactions.objects.filter(accounts=self.kwargs['accounts_id'])


class CategoryListForMakeTransaction(LoginRequiredMixin, ListView):
    model = TransactionsType.objects.filter()
    template_name = 'transactions/category_list_for_make_transaction.html'
    context_object_name = 'categories'
    allow_empty = False
    login_url = '/login/'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        transactions_type = TransactionsType.objects.filter()
        context['expenditure'] = transactions_type.filter(owner=self.request.user, main_type=False)
        context['income'] = transactions_type.filter(owner=self.request.user, main_type=True)
        context['title'] = 'Выбор категории'
        context['accounts'] = Accounts.objects.filter(owner=self.request.user)
        return context

    def get_queryset(self):
        return TransactionsType.objects.filter(owner=self.request.user)
        # return super().get_queryset().filter(owner=self.request.user.id)


class CreateTransaction(LoginRequiredMixin, CreateView):
    form_class = TransactionFrom
    template_name = 'transactions/add_transactions.html'
    success_url = reverse_lazy('transactions_home')
    login_url = '/admin/'

    def get_form(self, form_class=TransactionFrom):
        category = TransactionsType.objects.filter(id=self.kwargs['category_id']).first()
        form = super().get_form(form_class=form_class)
        accounts = Accounts.objects.filter(owner=self.request.user, currency=category.currency)
        form.fields['accounts'].queryset = accounts
        form.fields['accounts'].initial = accounts.first()
        form.fields['transactions_type'].queryset = TransactionsType.objects.filter(owner=self.request.user).filter(
            main_type=category.main_type)
        form.fields['transactions_type'].initial = category
        form.fields['money_value'].label = "Денежная сумма"
        return form

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['accounts'] = Accounts.objects.filter(owner=self.request.user)
        context['category'] = TransactionsType.objects.filter(id=self.kwargs['category_id']).first()
        return context

    def get_queryset(self):
        return TransactionsType.objects.filter(owner=self.request.user)


class CreateAccount(LoginRequiredMixin, CreateView):
    form_class = AccountForm
    template_name = 'transactions/add_account.html'
    success_url = reverse_lazy('transactions_home')
    login_url = '/admin/'

    def get_form(self, form_class=AccountForm):
        form = super().get_form(form_class=form_class)
        form.fields['balans'].label = "Баланс счёта"
        return form

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['accounts'] = Accounts.objects.filter(owner=self.request.user)
        return context

    def get_queryset(self):
        return TransactionsType.objects.filter(owner=self.request.user)


class CreateTransactionType(CreateView):
    form_class = TransactionTypeForm
    template_name = 'transactions/add_transactions_type.html'
    success_url = reverse_lazy('transactions_home')
    login_url = '/admin/'

    def form_valid(self, form):
        form.instance.owner = self.request.user
        main_type = self.kwargs.get('main_type', None)
        if main_type is not None:  # если аргумент существует
            if main_type == "True":
                form.instance.main_type = True
            else:
                form.instance.main_type = False  # фильтруем по нему посты
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['accounts'] = Accounts.objects.filter(owner=self.request.user)
        context['icons'] = Icons.objects.exclude(unicode='---')
        context['main_type'] = self.kwargs.get('main_type', None)
        return context

    def get_queryset(self):
        return TransactionsType.objects.filter(owner=self.request.user)


