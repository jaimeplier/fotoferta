# Generated by Django 2.2.2 on 2019-08-08 17:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('config', '0041_auto_20190730_1904'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orden',
            name='costo_envio',
            field=models.FloatField(default=99),
        ),
    ]
