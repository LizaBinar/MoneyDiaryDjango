# Generated by Django 4.1 on 2022-09-20 10:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0019_remove_icons_file'),
    ]

    operations = [
        migrations.AddField(
            model_name='icons',
            name='file',
            field=models.CharField(db_index=True, default='qweerty', max_length=50, verbose_name='Наименование файла'),
            preserve_default=False,
        ),
    ]
