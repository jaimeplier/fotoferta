# Generated by Django 2.2.2 on 2019-07-01 23:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('config', '0002_auto_20190628_2254'),
    ]

    operations = [
        migrations.AddField(
            model_name='codigomarco',
            name='estatus',
            field=models.BooleanField(default=True),
        ),
    ]
