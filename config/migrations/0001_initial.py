# Generated by Django 2.0.6 on 2019-06-26 22:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0009_alter_user_last_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Rol',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=64)),
            ],
            options={
                'managed': True,
                'db_table': 'rol',
            },
        ),
        migrations.CreateModel(
            name='RolHasPermissions',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('permission', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='auth.Permission')),
                ('rol', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='config.Rol')),
            ],
            options={
                'managed': True,
                'db_table': 'rol_has_permissions',
            },
        ),
        migrations.CreateModel(
            name='Usuario',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('nombre', models.CharField(max_length=64)),
                ('correo', models.EmailField(max_length=128, unique=True)),
                ('password', models.CharField(max_length=512)),
                ('estatus', models.BooleanField(default=True)),
                ('fecha_registro', models.DateField(auto_now_add=True)),
                ('customer_id', models.CharField(blank=True, max_length=45, null=True)),
                ('rol', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='config.Rol')),
            ],
            options={
                'managed': True,
                'db_table': 'usuario',
            },
        ),
        migrations.AddField(
            model_name='rol',
            name='permisos',
            field=models.ManyToManyField(through='config.RolHasPermissions', to='auth.Permission'),
        ),
    ]
