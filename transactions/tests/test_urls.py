from django.test import SimpleTestCase
from django.urls import reverse, resolve

from transactions.views import HomePage, TransactionDetail, AccountDetail, CategoryListForMakeTransaction, \
    CreateTransaction, CreateAccount, upload_exel, TransactionChartAPIView, CreateTransactionType


class TestUrls(SimpleTestCase):

    def test_transactions_home_urls_is_resolved(self):
        url = reverse('transactions_home')
        self.assertEqual(resolve(url).func.view_class, HomePage)

    def test_transaction_detail_urls_is_resolved(self):
        url = reverse('transaction_detail', args=[3])
        self.assertEqual(resolve(url).func.view_class, TransactionDetail)

    def test_account_detail_urls_is_resolved(self):
        url = reverse('account_detail', args=[3])
        self.assertEqual(resolve(url).func.view_class, AccountDetail)

    def test_add_transaction_detail_urls_is_resolved(self):
        url = reverse('add_transaction', args=[3])
        self.assertEqual(resolve(url).func.view_class, CreateTransaction)

    def test_add_account_detail_urls_is_resolved(self):
        url = reverse('add_account')
        self.assertEqual(resolve(url).func.view_class, CreateAccount)

    def test_add_transaction_type_detail_urls_is_resolved(self):
        url = reverse('add_transaction_type', args=[3])
        self.assertEqual(resolve(url).func.view_class, CreateTransactionType)

    def test_upload_exel_detail_urls_is_resolved(self):
        url = reverse('upload_exel')
        self.assertEqual(resolve(url).func, upload_exel)

    # def test_choice_category_detail_urls_is_resolved(self):
    #     url = reverse('choice_category')
    #     self.assertEqual(resolve(url).func.view_class, CategoryListForMakeTransaction)

    def test_make_income_expenditure_detail_urls_is_resolved(self):
        url = reverse('make_income_expenditure')
        self.assertEqual(resolve(url).func.view_class, TransactionChartAPIView)




