

class TransactionsLogic:

    def __init__(self, account, money_value, transactions):
        self.account = account
        self.money_value = money_value
        self.transactions = transactions

    def update_balans_post_delete(self):
        self.account.balans -= self.money_value
        return self.account.save()

    def update_balans_post_update_transactions(self):
        account = self.account
        get_all_money_value = self.transactions
        while True:
            account.balans = 0
            try:
                for i in range(10000000000000):
                    all_money = get_all_money_value.values('money_value')[i]['money_value']
                    account.balans += all_money
                    print(all_money)
            except IndexError:
                return account.save()

    def update_balans_post_save_new_transactions(self):
        self.account.balans += self.money_value
        self.account.save()
