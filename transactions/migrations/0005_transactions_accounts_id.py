# Generated by Django 4.1 on 2022-08-25 10:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0004_alter_accountstype_options_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='transactions',
            name='accounts_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='transactions.accounts', verbose_name='Счёт транзакции'),
        ),
    ]
