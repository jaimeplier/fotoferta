# Generated by Django 2.2.2 on 2019-07-03 23:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('config', '0018_fotografo_fotopartner'),
    ]

    operations = [
        migrations.AddField(
            model_name='fotografo',
            name='terminos_condiciones',
            field=models.BooleanField(default=0),
            preserve_default=False,
        ),
    ]
