# Generated by Django 2.2.2 on 2019-07-02 19:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('config', '0005_producto_tipo_papel'),
    ]

    operations = [
        migrations.AddField(
            model_name='orden',
            name='promocion',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='config.Promocion'),
        ),
        migrations.AddField(
            model_name='producto',
            name='promocion_aplicada',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='config.Promocion'),
        ),
    ]
