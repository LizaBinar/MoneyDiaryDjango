# from decimal import Decimal
from decimal import Decimal

# from django.contrib.auth.models import User
from django.test import TestCase, Client

from transactions.forms import TransactionForm, TransactionTypeForm, AccountForm
from transactions.models import Currency, Icons, TransactionsType, Accounts  # TransactionsType, Accounts, AccountsType


class TestTransactionForm(TestCase):
    databases = '__all__'
    fixtures = ['start_icons.json']

    # def test_expense_form_valid_data(self):
    #     self.client = Client
    #     self.user = User.objects.create_user('test_user', password='test_pass')
    #     self.client.login(username='test_user', password='test_pass')
    #     self.currency = Currency.objects.create(
    #         pk=1,
    #         title="SF coin",
    #     )
    #     self.currency = Currency.objects.create(
    #         pk=2,
    #         title="MD coin",
    #     )
    #     self.account_SF = Accounts.objects.create(
    #         pk=1,
    #         title="Uragan Bank Zakviel",
    #         balans=0,
    #         owner=self.user,
    #         currency_id=1
    #     )
    #     self.account_SF = Accounts.objects.create(
    #         pk=2,
    #         title="Uragan Bank Zakviel",
    #         balans=0,
    #         owner=self.user
    #     )
    #     self.transaction_type = TransactionsType.objects.create(
    #         pk=1,
    #         main_type=True,
    #         category="brains",
    #         owner=self.user,
    #         currency_id=1
    #     )
    #     form = TransactionForm(data={
    #         "money_value": Decimal(1000.44),
    #         "transactions_type": self.transaction_type,
    #         "accounts": self.account_SF
    #     })
    #
    #     self.assertTrue(form.is_valid())

    def test_transaction_type_form_no_data(self):
        # print(Icons.objects.first())
        form = TransactionTypeForm(data={})
        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors), 3)

    def test_account_form_no_data(self):
        form = AccountForm(data={})

        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors), 3)

    def test_transaction_form_no_data(self):
        self.client = Client()
        self.client.login(username='test_user', password='test_pass')
        form = TransactionForm()
        self.assertFalse(form.is_valid())

    def test_transaction_type_form_valid_data(self):
        sf_currency = Currency.objects.create(
            title='SF coin'
        )
        icon = Icons.objects.create(
            title='SF icon'
        )
        form = TransactionTypeForm(data={
            "category": 'tresh',
            "currency": sf_currency,
            "icons": icon
        })
        self.assertTrue(form.is_valid())

    # def test_transaction_form_valid_data(self):
    #     transaction_type = TransactionsType.objects.last()
    #     account = Accounts.objects.first()
    #     form = TransactionForm(data={
    #         "money_value": Decimal(1000.33),
    #         "transactions_type": transaction_type,
    #         "accounts": account,
    #         "comment": "qwerty"
    #     })
    #     self.assertTrue(form.is_valid())

    # def test_transaction_form_no_data(self):
    #     form = TransactionForm(data={})
    #
    #     self.assertFalse(form.is_valid())
    # self.assertEquals(len(form.errors), 3)
