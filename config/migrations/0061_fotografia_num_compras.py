# Generated by Django 2.2.2 on 2019-09-03 17:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('config', '0060_auto_20190902_1620'),
    ]

    operations = [
        migrations.AddField(
            model_name='fotografia',
            name='num_compras',
            field=models.BigIntegerField(default=0),
        ),
    ]