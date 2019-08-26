# Generated by Django 2.2.2 on 2019-08-26 23:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('config', '0057_fotografia_gratuita'),
    ]

    operations = [
        migrations.CreateModel(
            name='Genero',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=512)),
                ('fecha_alta', models.DateTimeField(auto_now_add=True)),
                ('fecha_baja', models.DateTimeField(blank=True, null=True)),
                ('fecha_actualizacion', models.DateTimeField(auto_now=True)),
                ('estatus', models.BooleanField(default=True)),
            ],
            options={
                'db_table': 'genero',
                'managed': True,
            },
        ),
    ]
