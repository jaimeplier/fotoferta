# Generated by Django 2.2.2 on 2019-07-03 20:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('config', '0012_auto_20190703_2050'),
    ]

    operations = [
        migrations.AlterField(
            model_name='modelomarialuisa',
            name='modelo',
            field=models.CharField(max_length=6, unique=True),
        ),
    ]
