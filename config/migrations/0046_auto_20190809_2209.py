# Generated by Django 2.2.2 on 2019-08-09 22:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('config', '0045_producto_tamanio'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tarjeta',
            name='nombre_propietario',
            field=models.CharField(max_length=32),
        ),
    ]
