from decimal import Decimal

from django.contrib.auth.models import User
from django.test import TestCase, Client

from transactions.models import Transactions, TransactionsType, Accounts, Currency, AccountsType


class TestTransactionModel(TestCase):
    fixtures = ['start_icons.json', ]

    def setUp(self):
        self.user = User.objects.create_user('test_user', password='test_pass')
        self.client = Client()
        self.client.login(username='test_user', password='test_pass')
        self.incom_type = TransactionsType.objects.last()

        # self.currency = Currency.objects.create(
        #     pk=1,
        #     title="SF coin",
        # )
        # self.currency = Currency.objects.create(
        #     pk=2,
        #     title="MD coin",
        # )
        # self.account_SF = Accounts.objects.create(
        #     pk=1,
        #     title="Uragan Bank Zakviel",
        #     balans=0,
        #     owner=self.user
        # )
        # self.account_SF = Accounts.objects.create(
        #     pk=2,
        #     title="Uragan Bank Zakviel",
        #     balans=0,
        #     owner=self.user
        # )
        # self.transaction_type = TransactionsType.objects.create(
        #     pk=1,
        #     main_type=True,
        #     category="brains",
        #     owner=self.user,
        # )

    def test_change_balans_after_create_new_transaction(self):
        transaction_income = Transactions.objects.create(
            pk=3,
            money_value=Decimal(1000.00),
            comment="don't read me please, ok?",
            accounts_id=2,
            transactions_type=self.incom_type,
            owner=self.user
        )
        self.assertEqual(Accounts.objects.get(pk=2).balans, 1000)
        self.assertEqual(transaction_income.save(), None)

    # def test_saved_good_transaction(self):
    #     transaction_income = Transactions.objects.create(
    #         pk=4,
    #         transactions_type_id=9,
    #         money_value=Decimal(1000.00),
    #         comment="don't read me please, ok?",
    #         accounts_id=2,
    #         owner=self.user
    #     )
    #     self.assertEqual(transaction_income.save(), None)

    def test_protect_of_transaction_by_transaction_type_main_type(self):
        bad_transaction = Transactions.objects.create(
            pk=6,
            money_value=Decimal(-1000.00),  # expenditure value
            comment="don't read me please, ok?",
            accounts_id=2,
            transactions_type=self.incom_type,  # transaction_type.main_type == True. It,s income type
            owner=self.user
        )
        self.assertEqual(bad_transaction.save(), False)

    def test_protect_of_transaction_by_currency(self):

        accounts_dollar = Accounts.objects.create(
            pk=10,
            balans=Decimal(0),
            title="account_dollar",
            accounts_type_id=2,
            currency_id=2,
            owner=self.user
        )
        bad_transaction = Transactions.objects.create(
            transactions_type=self.incom_type,
            pk=10,
            money_value=Decimal(1000.00),
            comment="don't read me please, ok?",
            accounts=accounts_dollar,
            owner=self.user
        )
        self.assertEqual(bad_transaction.save(), False)

