# Generated by Django 4.1 on 2022-09-01 18:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0011_accounts_balans'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='transactions',
            name='currency',
        ),
    ]
