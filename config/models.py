from __future__ import unicode_literals

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import Permission
from django.db import models

class UsuarioManager(BaseUserManager):
    def create_user(self, correo, password, rol, nombre):
        if not correo:
            raise ValueError('El usuario necesita un correo')

        user = self.model(
            correo=self.normalize_email(correo)
        )
        user.rol = rol
        user.nombre = nombre
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, correo, password, rol, nombre):
        user = self.create_user(correo=correo, password=password, rol=Rol(pk=1), nombre=nombre)
        user.save(using=self._db)
        return user

    def all_users(self):
        return super(UsuarioManager, self).get_queryset().all()


class Usuario(AbstractBaseUser):
    nombre = models.CharField(max_length=64)
    correo = models.EmailField(unique=True, max_length=128)
    password = models.CharField(max_length=512)
    rol = models.ForeignKey('Rol', models.DO_NOTHING)
    estatus = models.BooleanField(default=True)
    fecha_registro = models.DateField(auto_now_add=True)
    customer_id = models.CharField(max_length=45, blank=True, null=True)

    objects = UsuarioManager()

    USERNAME_FIELD = 'correo'
    REQUIRED_FIELDS = ['password', 'rol', 'nombre']

    def __str__(self):
        return self.correo

    def has_perm(self, perm, obj=None):
        if self.is_superuser:
            return True
        p = perm.split('.')
        if len(p) > 1:
            per = self.rol.permisos.filter(codename=p[1]).count()
        else:
            per = self.rol.permisos.filter(codename=p[0]).count()
        if per > 0:
            return True
        return False

    def has_perms(self, perm, obj=None):
        # Este válida
        if self.is_superuser:
            return True
        for p in perm:
            pr = p.split('.')
            if len(pr) > 1:
                per = self.rol.permisos.filter(codename=pr[1]).count()
            else:
                per = self.rol.permisos.filter(codename=pr[0]).count()
            if per == 0:
                return False
        return True

    def has_module_perms(self, app_label):
        if self.is_superuser:
            return True
        if self.is_staff:
            return True
        if self.rol.permisos.filter(codename=app_label).count() > 0:
            return True
        return False

    @property
    def is_staff(self):
        if self.rol.pk == 1:
            return True
        else:
            return False

    @property
    def is_superuser(self):
        if self.rol.pk == 1:
            return True
        else:
            return False

    @property
    def is_active(self):
        return self.estatus

    def get_full_name(self):
        return str(self.nombre)

    def get_short_name(self):
        return self.correo

    class Meta:
        managed = True
        db_table = 'usuario'

class Rol(models.Model):
    nombre = models.CharField(max_length=64)
    permisos = models.ManyToManyField(Permission, through='RolHasPermissions')

    def __str__(self):
        return self.nombre

    class Meta:
        managed = True
        db_table = 'rol'


class RolHasPermissions(models.Model):
    rol = models.ForeignKey(Rol, models.DO_NOTHING)
    permission = models.ForeignKey(Permission, models.DO_NOTHING)

    class Meta:
        managed = True
        db_table = 'rol_has_permissions'
