from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User


# class CurrencyType(models.Model):
#     title = True


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
    title = models.CharField(max_length=60, db_index=True, verbose_name="Наименование счета")
    owner_id = models.ForeignKey(User, on_delete=models.PROTECT, null=True, verbose_name='Владелец счёта')
    accounts_type_id = models.ForeignKey(AccountsType, on_delete=models.PROTECT, null=True, verbose_name="Тип счёта")
    currency_id = models.ForeignKey(Currency, on_delete=models.PROTECT, null=True, verbose_name="Валюта счёта")

    def get_absolute_url(self):
        return reverse('accounts', kwargs={"accounts_id": self.pk})

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Счёт"
        verbose_name_plural = "Cчёты"
        ordering = ['title']


class TransactionsType(models.Model):
    main_type = models.CharField(max_length=10, db_index=True, verbose_name="Главный тип")
    category = models.CharField(max_length=60, db_index=True, verbose_name="Категория")
    currency_id = models.ForeignKey(Currency, on_delete=models.PROTECT, null=True, verbose_name="Валюта транзакции")
    owner_id = models.ForeignKey(User, on_delete=models.PROTECT, null=True, verbose_name='Владелец типа')

    def get_absolute_url(self):
        return reverse('transactions_type', kwargs={"transactions_type_id": self.pk})

    def __str__(self):
        result = (str(self.main_type) + ' ' + str(self.category))
        return result

    class Meta:
        verbose_name = "Тип транзакций"
        verbose_name_plural = "Типы транзакций"
        ordering = ['main_type']


class Transactions(models.Model):
    money_value = models.PositiveBigIntegerField(verbose_name='Денежная сумма')
    comment = models.TextField(verbose_name='Примечание к транзакции')
    owner_id = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        null=True,
        verbose_name='Владелец транзакции')
    data_time = models.DateTimeField(auto_now_add=True, verbose_name="Дата совершения транзакции")
    currency_id = models.ForeignKey(Currency, on_delete=models.PROTECT, null=True, verbose_name="Валюта транзакции")
    transactions_type_id = models.ForeignKey(
        TransactionsType,
        on_delete=models.PROTECT,
        null=True,
        verbose_name="Тип транзакции"
    )
    accounts_id = models.ForeignKey(
        Accounts,
        on_delete=models.PROTECT,
        null=True,
        verbose_name="Счёт транзакции"
    )

    def get_absolute_url(self):
        return reverse('transactions', kwargs={"pk": self.pk})

    def __str__(self):
        return str(self.money_value)

    class Meta:
        verbose_name = "Транзакция"
        verbose_name_plural = "Транзакции"
        ordering = ['-data_time']
