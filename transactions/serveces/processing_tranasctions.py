class TransactionsLogic:

    def __init__(self, account, money_value):
        self.account = account
        self.money_value = money_value

    def update_balans(self):
        account = self.account
        account.balans += self.money_value
        return account.save()
