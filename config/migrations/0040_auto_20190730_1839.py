# Generated by Django 2.2.2 on 2019-07-30 18:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('config', '0039_auto_20190730_1830'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tamanio',
            name='alto',
        ),
        migrations.RemoveField(
            model_name='tamanio',
            name='ancho',
        ),
        migrations.RemoveField(
            model_name='tamanio',
            name='area',
        ),
    ]
