# Generated by Django 2.2.2 on 2019-07-11 16:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('config', '0030_auto_20190711_1620'),
    ]

    operations = [
        migrations.AddField(
            model_name='papelimpresion',
            name='estatus',
            field=models.BooleanField(default=True),
        ),
    ]
