# Generated by Django 2.2.2 on 2019-07-03 21:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('config', '0013_auto_20190703_2059'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='marialuisa',
            name='modelo',
        ),
    ]
