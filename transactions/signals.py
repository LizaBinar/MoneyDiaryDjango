from django.contrib.auth.models import User
from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver

from transactions.models import Accounts, TransactionsType, Icons, AccountsType, Currency, Transactions
from transactions.serveces.processing_tranasctions import TransactionsLogic


@receiver(pre_delete, sender=Transactions)  # , dispatch_uid='question_delete_signal')
def delete_transactions(sender, instance, using, **kwargs):
    transactions_logic = TransactionsLogic(account=instance.accounts, money_value=instance.money_value,
                                           transactions=Transactions.objects.filter(owner=instance.owner,
                                                                                    transactions_type__currency=instance.transactions_type.currency,
                                                                                    accounts=instance.accounts))
    transactions_logic.update_balans_post_delete()


@receiver(post_save, sender=Transactions)
def save_transactions(sender, instance, created, **kwargs):
    if created:
        transactions_logic = TransactionsLogic(account=instance.accounts, money_value=instance.money_value,
                                               transactions=Transactions.objects.filter(owner=instance.owner,
                                                                                        transactions_type__currency=instance.transactions_type.currency,
                                                                                        accounts=instance.accounts))
        return transactions_logic.update_balans_post_save_new_transactions()
    else:
        transactions_logic = TransactionsLogic(account=instance.accounts, money_value=instance.money_value,
                                               transactions=Transactions.objects.filter(owner=instance.owner,
                                                                                        transactions_type__currency=instance.transactions_type.currency,
                                                                                        accounts=instance.accounts))
        return transactions_logic.update_balans_post_update_transactions()


# self.transactions_logic = TransactionsLogic(account=self.accounts, money_value=self.money_value, transactions=Transactions.objects.filter(owner=self.owner, transactions_type__currency=self.transactions_type.currency, accounts=self.accounts))
# self.transactions_logic.update_balans()


@receiver(post_save, sender=Accounts)
def save_account(sender, instance, created, **kwargs):
    print(sender)
    if len(Accounts.objects.filter(owner=instance.owner, currency=instance.currency)) == 1:
        expenditure_svg_id = ['Корзинка', 'Горячая чашка', 'Кинопленка', 'Транспорт', 'Сердце', 'Люди', 'Магазин',
                              'Подарок']
        income_svg_id = ['Деньги в руке', 'Человек с монетой', 'Портфель', 'Подарок']
        item_address = 0
        for title in ['Продукты', 'Кафе', 'Досуг', 'Транспорт', 'Здоровье', 'Семья', 'Покупки', 'Подарки']:
            TransactionsType.objects.create(main_type=False, category=title, currency=instance.currency,
                                            owner=instance.owner,
                                            icons=Icons.objects.get(title=expenditure_svg_id[item_address]))
            item_address += 1
        item_address = 0
        for title in ['Зарплата', 'Фриланс', 'Бизнес', 'Подарки']:
            TransactionsType.objects.create(main_type=True, category=title, currency=instance.currency,
                                            owner=instance.owner,
                                            icons=Icons.objects.get(title=income_svg_id[item_address]))
            item_address += 1


@receiver(post_save, sender=User)
def save_or_create_profile(sender, instance, created, **kwargs):
    print(sender)
    print(instance)
    print(created)
    base_currency = Currency.objects.get(title='₽')
    expenditure_svg_id = ['Корзинка', 'Горячая чашка', 'Кинопленка', 'Транспорт', 'Сердце', 'Люди', 'Магазин',
                          'Подарок']
    income_svg_id = ['Деньги в руке', 'Человек с монетой', 'Портфель', 'Подарок']
    item_address = 0
    if created:
        for title in ['Продукты', 'Кафе', 'Досуг', 'Транспорт', 'Здоровье', 'Семья', 'Покупки', 'Подарки']:
            TransactionsType.objects.create(main_type=False, category=title, currency=base_currency, owner=instance,
                                            icons=Icons.objects.get(title=expenditure_svg_id[item_address]))
            item_address += 1
        item_address = 0
        for title in ['Зарплата', 'Фриланс', 'Бизнес', 'Подарки']:
            TransactionsType.objects.create(main_type=True, category=title, currency=base_currency, owner=instance,
                                            icons=Icons.objects.get(title=income_svg_id[item_address]))
            item_address += 1

        Accounts.objects.create(balans=0, title='Кошелёк', currency=base_currency, owner=instance,
                                accounts_type=AccountsType.objects.filter(pk=1).first())
        Accounts.objects.create(balans=0, title='Карточка', currency=base_currency, owner=instance,
                                accounts_type=AccountsType.objects.filter(pk=2).first())

    # else:
    #     try:
    #         instance.profile.save()
    #     except ObjectDoesNotExist:
    #         TransactionsType.objects.create(user=instance)
