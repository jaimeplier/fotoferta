# Generated by Django 2.2.2 on 2019-07-04 17:47

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('config', '0019_fotografo_terminos_condiciones'),
    ]

    operations = [
        migrations.CreateModel(
            name='PersonalAdministrativo',
            fields=[
                ('usuario_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'managed': True,
                'db_table': 'personal_administrativo',
            },
            bases=('config.usuario',),
        ),
    ]
