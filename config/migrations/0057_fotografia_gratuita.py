# Generated by Django 2.2.2 on 2019-08-26 23:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('config', '0056_auto_20190822_2234'),
    ]

    operations = [
        migrations.AddField(
            model_name='fotografia',
            name='gratuita',
            field=models.BooleanField(default=False),
        ),
    ]
