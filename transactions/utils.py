from transactions.models import Transactions, Accounts, Icons

title = "title_text"


class TransactionMixin:

    def get_basic_transactions_context(self, user, **kwargs):
        context = kwargs
        transactions = Transactions.objects.filter(owner=user)
        accounts = Accounts.objects.filter(owner=user)
        icons = Icons.objects.exclude(unicode='---')
        context['user'] = user
        context['transactions'] = transactions
        context['accounts'] = accounts
        context[icons] = icons
        return context
