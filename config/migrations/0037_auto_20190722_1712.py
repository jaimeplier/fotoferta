# Generated by Django 2.2.2 on 2019-07-22 17:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('config', '0036_auto_20190722_1708'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orden',
            name='costo_envio',
            field=models.FloatField(default=96),
        ),
    ]
