# Generated by Django 2.2.2 on 2019-07-02 22:11

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('config', '0008_auto_20190702_2155'),
    ]

    operations = [
        migrations.AddField(
            model_name='fotografo',
            name='foto_portada',
            field=models.ImageField(blank=True, null=True, upload_to='foto_portada/', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['png', 'jpg'])]),
        ),
        migrations.AddField(
            model_name='marialuisa',
            name='imagen',
            field=models.ImageField(default='img', upload_to='img_marialuisa/', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['png', 'jpg'])]),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='usuario',
            name='foto_perfil',
            field=models.ImageField(blank=True, null=True, upload_to='foto_perfil/', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['png', 'jpg'])]),
        ),
    ]
