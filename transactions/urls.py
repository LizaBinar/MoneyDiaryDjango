from django.urls import path

from . import views

urlpatterns = [
    path('', views.HomePage.as_view(), name='transactions_home'),
    path('transaction/<int:pk>/', views.TransactionDetail.as_view(), name='transaction_detail'),
    # path('transactions_type/<int:transactions_type_id>/', TransactionsByCategory.as_view(extra_context={'title': 'Какой-то тайтл'}), name='category'),
    path('accounts/<int:pk>/', views.AccountDetail.as_view(), name='account_detail'),
    path('choice_account/', views.AccountListForMakeTransaction.as_view(extra_context={'title': 'Выбор категории'}),
         name='choice_account'),
    path('choice_сategory/<int:account_id>/', views.CategoryListForMakeTransaction.as_view(extra_context={'title': 'Выбор категории'}),
         name='choice_category'),
    path('add_transaction/<int:category_id>/', views.CreateTransaction.as_view(), name='add_transaction'),
    path('add_account/', views.CreateAccount.as_view(), name='add_account'),
    path('add_transaction_type/<str:main_type>/', views.CreateTransactionType.as_view(), name='add_transaction_type'),
    path('get_xlsx_file/', views.upload_exel, name="upload_exel"),

    path('make_income_expenditure/<int:id_currency>/', views.TransactionChartAPIView.as_view(), name='make_income_expenditure'),

    path('transactions/<int:pk>/update', views.UpdateTransaction.as_view(), name='transactions_update'),
    path('transactions/<int:pk>/delete', views.DeleteTransaction.as_view(), name='transactions_delete'),

]
