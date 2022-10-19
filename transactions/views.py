import datetime
from urllib.parse import urlencode

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Sum
from django.http import QueryDict, HttpResponse
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView  # , UpdateView
# from qsstats import QuerySetStats
from rest_framework.response import Response
from rest_framework.views import APIView

from transactions.forms import TransactionForm, AccountForm, TransactionTypeForm
from transactions.models import Transactions, Accounts, TransactionsType, Currency  # , Icons
from transactions.serveces.make_chart import ChartsLogic
from transactions.serveces.make_exel import make_xlsx_file_in_response
from transactions.utils import TransactionMixin


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


class TransactionChartAPIView(APIView):

    def get(self, request, title):
        currency = Currency.objects.get(title=self.kwargs['title'])
        chart_logic = ChartsLogic()
        transactions = Transactions.objects.filter(owner=request.user, transactions_type__currency=currency)
        ratio_chart = chart_logic.make_chart(transactions=transactions, grouping_by_date='data_time__date')
        return Response({'label': ratio_chart['label'], 'income_data': ratio_chart['income_data'],
                         'expenditure_data': ratio_chart['expenditure_data']})


class HomePage(LoginRequiredMixin, TransactionMixin, ListView):
    model = Transactions
    template_name = "transactions/home_transactions_list.html"
    context_object_name = 'transactions'
    queryset = 'category'

    def get_context_data(self, *, object_list=None, **kwargs):
        accounts = Accounts.objects.filter(owner=self.request.user)
        base_context = self.get_basic_transactions_context(title="Главная панель", user=self.request.user)
        context = super().get_context_data(**kwargs)
        context['month'] = datetime.datetime.now()
        context['sum_balans'] = QueryDict(urlencode(sum_balans(accounts)))
        context = dict(list(context.items()) + list(base_context.items()))
        return context


class TransactionDetail(LoginRequiredMixin, TransactionMixin, DetailView):
    model = Transactions  # pk=self.kwargs['category_id'])
    template_name = 'transactions/transactions_detail.html'
    # context_object_name = 'transaction'
    allow_empty = False

    # login_url = '/users/logout/'

    def get_context_data(self, *, object_list=None, **kwargs):
        base_context = self.get_basic_transactions_context(title="Детали транзакции", user=self.request.user)
        context = super().get_context_data(**kwargs)
        context['transaction_one'] = Transactions.objects.get(pk=self.kwargs['pk'])
        context = dict(list(context.items()) + list(base_context.items()))
        return context


class AccountDetail(LoginRequiredMixin, TransactionMixin, DetailView):  # MyMixin
    model = Accounts
    template_name = "transactions/account_detail.html"
    allow_empty = False

    def get_context_data(self, *, object_list=None, **kwargs):
        base_context = self.get_basic_transactions_context(title="Счёт", user=self.request.user)
        context = super().get_context_data(**kwargs)
        context['account'] = Accounts.objects.get(pk=self.kwargs['pk'])
        context = dict(list(context.items()) + list(base_context.items()))
        return context


class AccountListForMakeTransaction(LoginRequiredMixin, TransactionMixin, ListView):
    model = Accounts
    template_name = 'transactions/account_list_for_make_transaction.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        base_context = self.get_basic_transactions_context(user=self.request.user, title="Выбор счёта")
        context = dict(list(context.items()) + list(base_context.items()))
        return context

    def get_queryset(self):
        return TransactionsType.objects.filter(owner=self.request.user)


class CategoryListForMakeTransaction(LoginRequiredMixin, TransactionMixin, ListView):
    model = TransactionsType.objects.filter()
    template_name = 'transactions/category_list_for_make_transaction.html'
    context_object_name = 'categories'
    allow_empty = False

    # login_url = '/users/logout/'

    def get_context_data(self, *, object_list=None, **kwargs):
        account = Accounts.objects.get(id=self.kwargs['account_id'])
        context = super().get_context_data(**kwargs)
        base_context = self.get_basic_transactions_context(title="Выбор категории", user=self.request.user)
        transactions_type = TransactionsType.objects.filter(owner=self.request.user, currency=account.currency)
        context['expenditure'] = transactions_type.filter(main_type=False)
        context['income'] = transactions_type.filter(main_type=True)
        context = dict(list(context.items()) + list(base_context.items()))
        return context

    def get_queryset(self):
        return TransactionsType.objects.filter(owner=self.request.user)
        # return super().get_queryset().filter(owner=self.request.user.id)


class CreateTransaction(LoginRequiredMixin, TransactionMixin, CreateView):
    form_class = TransactionForm
    template_name = 'transactions/add_transactions.html'
    success_url = reverse_lazy('transactions_home')

    # login_url = '/users/logout/'

    def get_form(self, form_class=TransactionForm):
        category = TransactionsType.objects.get(id=self.kwargs['category_id'])
        form = super().get_form(form_class=form_class)
        accounts = Accounts.objects.filter(owner=self.request.user, currency=category.currency)
        form.fields['accounts'].queryset = accounts
        form.fields['accounts'].initial = accounts.first()
        form.fields['transactions_type'].queryset = TransactionsType.objects.filter(owner=self.request.user,
                                                                                    currency=category.currency,
                                                                                    main_type=category.main_type)
        form.fields['transactions_type'].initial = category
        form.fields['money_value'].label = "Денежная сумма"
        return form

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        base_context = self.get_basic_transactions_context(title="Добавление транзакции", user=self.request.user)
        context['category'] = TransactionsType.objects.filter(id=self.kwargs['category_id']).first()
        context = dict(list(context.items()) + list(base_context.items()))
        return context

    def get_queryset(self):
        return TransactionsType.objects.filter(owner=self.request.user)


class CreateAccount(LoginRequiredMixin, TransactionMixin, CreateView):
    form_class = AccountForm
    template_name = 'transactions/add_account.html'
    success_url = reverse_lazy('transactions_home')

    # login_url = '/users/logout/'

    def get_form(self, form_class=AccountForm):
        form = super().get_form(form_class=form_class)
        form.fields['balans'].label = "Баланс счёта"
        return form

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        base_context = self.get_basic_transactions_context(title="Добавление счёта", user=self.request.user)
        context = dict(list(context.items()) + list(base_context.items()))
        return context

    def get_queryset(self):
        return TransactionsType.objects.filter(owner=self.request.user)


class CreateTransactionType(LoginRequiredMixin, TransactionMixin, CreateView):
    form_class = TransactionTypeForm
    template_name = 'transactions/add_transactions_type.html'
    success_url = reverse_lazy('transactions_home')

    # login_url = '/users/logout/'

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
        base_context = self.get_basic_transactions_context(title="Добавление транзакции", user=self.request.user)
        context['main_type'] = self.kwargs.get('main_type', None)
        context = dict(list(context.items()) + list(base_context.items()))
        return context

    def get_queryset(self):
        return TransactionsType.objects.filter(owner=self.request.user)


class UpdateTransaction(UpdateView):
    model = Transactions
    template_name = 'transactions/transaction_update.html'
    success_url = reverse_lazy('transactions_home')
    form_class = TransactionForm

    def get_form(self, form_class=TransactionForm):
        category = TransactionsType.objects.get(id=self.kwargs['pk'])
        form = super().get_form(form_class=form_class)
        accounts = Accounts.objects.filter(owner=self.request.user, currency=category.currency)
        form.fields['accounts'].queryset = accounts
        form.fields['accounts'].initial = accounts.first()
        form.fields['transactions_type'].queryset = TransactionsType.objects.filter(owner=self.request.user,
                                                                                    currency=category.currency,
                                                                                    main_type=category.main_type)
        form.fields['transactions_type'].initial = category
        form.fields['money_value'].label = "Денежная сумма"
        return form


class DeleteTransaction(DeleteView):
    model = Transactions
    template_name = 'transactions/transaction_delete.html'
    success_url = reverse_lazy('transactions_home')
