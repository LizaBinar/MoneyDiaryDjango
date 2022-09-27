# Generated by Django 4.1 on 2022-09-19 07:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0014_alter_transactionstype_main_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='transactionstype',
            name='icons',
            field=models.CharField(db_index=True, default=1, max_length=50, verbose_name='Иконка'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='transactions',
            name='comment',
            field=models.TextField(max_length=150, verbose_name='Примечание к транзакции'),
        ),
    ]
