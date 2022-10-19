from decimal import Decimal

from django.contrib.auth.models import User
from django.test import TestCase, Client
from django.urls import reverse

from transactions.models import Transactions, TransactionsType, Accounts, Currency


class TestViews(TestCase):
    fixtures = ['start_icons.json', ]

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user('test_user', password='test_pass')
        self.client.login(username='test_user', password='test_pass')

    def test_transaction_have_detail_GET(self):
        self.transaction = Transactions.objects.create(
            transactions_type=TransactionsType.objects.last(),
            pk=3,
            money_value=Decimal(1000.00),
            comment="don't read me please, ok?",
            accounts=Accounts.objects.first(),
            owner=self.user
        )
        response = self.client.get(reverse('transaction_detail', args=[3]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'transactions/transactions_detail.html')

    # def test_transaction_not_have_detail_GET(self):
    #     self.transaction = Transactions.objects.create(
    #         transactions_type_id=3,
    #         pk=4,
    #         money_value=Decimal(-1000.00),
    #         comment="don't read me please, ok?",
    #         accounts_id=3,
    #         owner=self.user
    #     )
    #     response = self.client.get(reverse('transaction_detail', args=[4]))
    #     self.assertEqual(response.status_code, 404)

    def test_home_page_list_GET(self):
        response = self.client.get(reverse('transactions_home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'transactions/home_transactions_list.html')

    def test_account_detail_GET(self):
        account_pk = Accounts.objects.first().pk
        response = self.client.get(reverse('account_detail', args=[account_pk]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'transactions/account_detail.html')

    def test_choice_category_GET(self):
        response = self.client.get(reverse('choice_category'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'transactions/category_list_for_make_transaction.html')

    def test_add_transaction_GET(self):
        transaction_type_pk = TransactionsType.objects.first().pk
        response = self.client.get(reverse('add_transaction', args=[transaction_type_pk]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'transactions/add_transactions.html')

    def test_add_account_GET(self):
        response = self.client.get(reverse('add_account'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'transactions/add_account.html')

    def test_add_transaction_type_GET(self):
        response = self.client.get(reverse('add_transaction_type', args=["True"]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'transactions/add_transactions_type.html')

    def make_income_expenditure(self):
        response = self.client.get(reverse('make_income_expenditure'))
        self.assertEqual(response.status_code, 200)




        # urlpatterns = [
        #     path('transactions/', views.HomePage.as_view(), name='transactions_home'),
        #     path('transaction/<int:pk>/', views.TransactionDetail.as_view(), name='transaction_detail'),
        #     # path('transactions_type/<int:transactions_type_id>/', TransactionsByCategory.as_view(extra_context={'title': 'Какой-то тайтл'}), name='category'),
        #     path('accounts/<int:pk>/', views.AccountDetail.as_view(), name='account_detail'),
        #     path('choice_сategory/', views.CategoryListForMakeTransaction.as_view(extra_context={'title': 'Выбор категории'}),
        #          name='choice_category'),
        #     path('add_transaction/<int:category_id>/', views.CreateTransaction.as_view(), name='add_transaction'),
        #     path('add_account/', views.CreateAccount.as_view(), name='add_account'),
        #     path('add_transaction_type/<str:main_type>/', views.CreateTransactionType.as_view(), name='add_transaction_type'),
        #     path('get_xlsx_file/', views.upload_exel, name="upload_exel"),
        #
        #     path('make_income_expenditure/', views.TransactionChartAPIView.as_view(), name='make_income_expenditure')
        # ]
