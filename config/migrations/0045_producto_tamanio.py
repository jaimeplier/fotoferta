# Generated by Django 2.2.2 on 2019-08-09 00:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('config', '0044_auto_20190808_1806'),
    ]

    operations = [
        migrations.AddField(
            model_name='producto',
            name='tamanio',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='config.Tamanio'),
        ),
    ]
