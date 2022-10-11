from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from transactions.models import Accounts, TransactionsType, Icons, AccountsType, Currency

# User = get_user_model()


@receiver(post_save, sender=User)
def save_or_create_profile(sender, instance, created, **kwargs):
    base_currency = Currency.objects.filter(title='₽').first()
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
