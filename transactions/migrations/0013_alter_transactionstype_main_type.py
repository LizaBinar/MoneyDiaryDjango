# Generated by Django 4.1 on 2022-09-02 12:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0012_remove_transactions_currency'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transactionstype',
            name='main_type',
            field=models.BooleanField(verbose_name='Главный тип'),
        ),
    ]
