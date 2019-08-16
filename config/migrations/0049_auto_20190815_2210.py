# Generated by Django 2.2.2 on 2019-08-15 22:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('config', '0048_tarjeta_eliminado'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='producto',
            name='tamanio',
        ),
        migrations.AddField(
            model_name='producto',
            name='foto_tamanio_precio',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='config.FotoPrecio'),
        ),
    ]