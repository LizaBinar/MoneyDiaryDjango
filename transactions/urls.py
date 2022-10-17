from django.urls import path
from .views import *


urlpatterns = [
    path('transactions/', MyTransactions.as_view(), name='transactions_home'),
    path('transaction/<int:pk>/', TransactionDetail.as_view(), name='transaction_detail'),
    # path('transactions_type/<int:transactions_type_id>/', TransactionsByCategory.as_view(extra_context={'title': 'Какой-то тайтл'}), name='category'),
    path('accounts/<int:pk>/', AccountDetail.as_view(), name='account_detail'),
    path('choice_сategory/', CategoryListForMakeTransaction.as_view(extra_context={'title': 'Выбор категории'}), name='choice_category'),
    path('add_transaction/<int:category_id>/', CreateTransaction.as_view(), name='add_transaction'),
    path('add_account/', CreateAccount.as_view(), name='add_account'),
    path('add_transaction_type/<str:main_type>/', CreateTransactionType.as_view(), name='add_transaction_type'),
    path('get_xlsx_file/', upload_exel, name="upload_exel"),

    path('make_income_expenditure/', TransactionChartAPIView.as_view(), name='make_income_expenditure'),

    path('transactions/<int:pk>/update', UpdateTransaction.as_view(), name='transactions_update'),
    path('transactions/<int:pk>/delete', DeleteTransaction.as_view(), name='transactions_delete'),
]


