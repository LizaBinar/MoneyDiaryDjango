# Generated by Django 4.1 on 2022-09-01 15:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0010_alter_transactions_money_value'),
    ]

    operations = [
        migrations.AddField(
            model_name='accounts',
            name='balans',
            field=models.BigIntegerField(default=0, verbose_name='Баланс счета'),
        ),
    ]
