# Generated by Django 2.2.2 on 2019-07-11 00:07

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('config', '0025_merge_20190711_0007'),
    ]

    operations = [
        migrations.AlterField(
            model_name='promocion',
            name='imagen',
            field=models.ImageField(blank=True, null=True, upload_to='promo_fotoferta/', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['png', 'jpg'])]),
        ),
    ]
