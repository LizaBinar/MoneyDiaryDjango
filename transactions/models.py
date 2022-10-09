from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse


# class CurrencyType(models.Model):
#     title = True

class Icons(models.Model):
    title = models.CharField(max_length=50, db_index=True, verbose_name="Наименование")
    file = models.CharField(max_length=50, db_index=True, verbose_name="Наименование файла")
    unicode = models.CharField(max_length=50, db_index=True, verbose_name="юникод символа")
    unicode_icons = models.CharField(max_length=50, db_index=True, verbose_name="дешифрованный юникод символа")

    def get_absolute_url(self):
        return reverse('icons', kwargs={"icons_id": self.pk})

    def __str__(self):
        return self.title + ' ' + self.unicode_icons

    class Meta:
        verbose_name = "иконка"
        verbose_name_plural = "иконки"
        ordering = ['title']


class Currency(models.Model):
    title = models.CharField(max_length=50, db_index=True, verbose_name="Наименование валюты")

    # type_id = True

    def get_absolute_url(self):
        return reverse('currency', kwargs={"currency_id": self.pk})

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Валюта"
        verbose_name_plural = "Валюты"
        ordering = ['title']


class AccountsType(models.Model):
    title = models.CharField(max_length=30, db_index=True, verbose_name="Наименование типа счётов")

    def get_absolute_url(self):
        return reverse('accounts_type', kwargs={"accounts_type_id": self.pk})

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Тип cчётов"
        verbose_name_plural = "Типы счётов"
        ordering = ['title']


class Accounts(models.Model):
    balans = models.DecimalField(verbose_name="Баланс счета", max_digits=17, decimal_places=2)
    title = models.CharField(max_length=60, db_index=True, verbose_name="Наименование счета")
    owner = models.ForeignKey(User, on_delete=models.PROTECT, null=True, verbose_name='Владелец счёта')
    accounts_type = models.ForeignKey(AccountsType, on_delete=models.PROTECT, null=True, verbose_name="Тип счёта")
    currency = models.ForeignKey(Currency, on_delete=models.PROTECT, null=True, verbose_name="Валюта счёта")

    def get_absolute_url(self):
        return reverse('accounts', kwargs={"accounts_id": self.pk})

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Счёт"
        verbose_name_plural = "Cчёты"
        ordering = ['title']


class TransactionsType(models.Model):
    main_type = models.BooleanField(verbose_name="Тип:")  # False - расход | True - Доход
    category = models.CharField(max_length=60, db_index=True, verbose_name="Категория")
    icons = models.ForeignKey(Icons, on_delete=models.PROTECT, null=True, verbose_name="Иконка")
    currency = models.ForeignKey(Currency, on_delete=models.PROTECT, null=True, verbose_name="Валюта транзакции")
    owner = models.ForeignKey(User, on_delete=models.PROTECT, null=True, verbose_name='Владелец типа')

    def get_absolute_url(self):
        return reverse('transactions_type', kwargs={"transactions_type_id": self.pk})

    def __str__(self):
        # main_type = ''
        if self.main_type:
            main_type = "Доход"
        else:
            main_type = "Расход"
        result = main_type + ' ' + str(self.category)
        return result

    class Meta:
        verbose_name = "Тип транзакций"
        verbose_name_plural = "Типы транзакций"
        ordering = ['main_type']


class Transactions(models.Model):
    money_value = models.DecimalField(verbose_name='Денежная сумма', max_digits=17, decimal_places=2)
    comment = models.TextField(verbose_name='Примечание к транзакции', max_length=150, blank=True)
    owner = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        null=True,
        verbose_name='Владелец транзакции')
    data_time = models.DateTimeField(auto_now_add=True, verbose_name="Дата совершения транзакции")
    # currency = models.ForeignKey(Currency, on_delete=models.PROTECT, null=True, verbose_name="Валюта транзакции")
    transactions_type = models.ForeignKey(
        TransactionsType,
        on_delete=models.PROTECT,
        null=True,
        verbose_name="Тип транзакции"
    )
    accounts = models.ForeignKey(
        Accounts,
        on_delete=models.PROTECT,
        null=True,
        verbose_name="Счёт транзакции"
    )

    def get_absolute_url(self):
        return reverse('transactions', kwargs={"pk": self.pk})

    def __str__(self):
        return str(self.money_value)

    def update_balans(self):
        new_balans = self.accounts
        new_balans.balans += self.money_value
        return new_balans.save()

    def save(self, *args, **kwargs):
        if (self.money_value == 0) or (self.money_value < 0 and self.transactions_type.main_type == True) or (
                self.money_value > 0 and self.transactions_type.main_type == False):
            return False
        super(Transactions, self).save(*args, **kwargs)
        instance = self.update_balans()
        return instance

    class Meta:
        verbose_name = "Транзакция"
        verbose_name_plural = "Транзакции"
        ordering = ['-data_time']


