# Generated by Django 2.2.2 on 2019-08-22 22:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('config', '0055_descarga_orden'),
    ]

    operations = [
        migrations.AlterField(
            model_name='descarga',
            name='token',
            field=models.CharField(max_length=256),
        ),
    ]
