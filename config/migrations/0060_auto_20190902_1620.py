# Generated by Django 2.2.2 on 2019-09-02 16:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('config', '0059_usuario_genero'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usuario',
            name='genero',
            field=models.ForeignKey(default=3, on_delete=django.db.models.deletion.DO_NOTHING, to='config.Genero'),
        ),
    ]