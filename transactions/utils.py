from transactions.models import Transactions, Accounts, Icons, TransactionsType, Currency

title = "title_text"


class TransactionMixin:

    def get_basic_transactions_context(self, user, **kwargs):
        context = kwargs
        transactions = Transactions.objects.filter(owner=user)
        accounts = Accounts.objects.filter(owner=user)
        icons = Icons.objects.exclude(unicode='---')
        currency = Currency.objects.all()
        context['user'] = user
        context['transactions'] = transactions
        context['accounts'] = accounts
        context['currency'] = currency
        context[icons] = icons
        return context

    # def get_basic_transactions_forms_data(self, user, **kwargs):
    #     data_for_forms = kwargs
    #     transactions = Transactions.objects.filter(owner=user)
    #     transaction_types = TransactionsType.objects.filter(owner=user)
    #     accounts = Accounts.objects.filter(owner=user)
    #     data_for_forms['transactions'] = transactions
    #     data_for_forms['transaction_types'] = transaction_types
    #     data_for_forms['accounts'] = accounts
    #     return data_for_forms
