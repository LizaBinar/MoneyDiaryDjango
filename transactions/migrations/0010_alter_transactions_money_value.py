# Generated by Django 4.1 on 2022-08-31 17:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0009_rename_accounts_type_id_accounts_accounts_type_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transactions',
            name='money_value',
            field=models.BigIntegerField(verbose_name='Денежная сумма'),
        ),
    ]