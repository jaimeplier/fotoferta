# Generated by Django 2.2.2 on 2019-07-11 15:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('config', '0027_contactanos'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tipopapel',
            name='grosor',
        ),
        migrations.RemoveField(
            model_name='producto',
            name='tipo_papel',
        ),
        migrations.DeleteModel(
            name='GrosorPapel',
        ),
        migrations.DeleteModel(
            name='TipoPapel',
        ),
    ]
