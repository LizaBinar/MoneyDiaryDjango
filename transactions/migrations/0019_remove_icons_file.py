# Generated by Django 4.1 on 2022-09-20 10:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0018_rename_address_icons_file_icons_unicode'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='icons',
            name='file',
        ),
    ]