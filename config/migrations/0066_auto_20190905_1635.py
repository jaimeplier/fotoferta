# Generated by Django 2.2.2 on 2019-09-05 16:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('config', '0065_notificacion_leido'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orden',
            name='fecha_compra',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
