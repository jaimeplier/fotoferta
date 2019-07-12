from __future__ import unicode_literals

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import Permission
from django.core.validators import FileExtensionValidator, MinValueValidator, MaxValueValidator
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
    foto_perfil = models.ImageField(upload_to='foto_perfil/',
                               validators=[FileExtensionValidator(allowed_extensions=['png', 'jpg'])], null=True, blank=True)
    nombre = models.CharField(max_length=64)
    correo = models.EmailField(unique=True, max_length=128)
    password = models.CharField(max_length=512)
    rol = models.ForeignKey('Rol', models.DO_NOTHING)
    estatus = models.BooleanField(default=True)
    fecha_registro = models.DateField(auto_now_add=True)
    customer_id = models.CharField(max_length=45, blank=True, null=True)
    confiable = models.BooleanField(default=False)

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
    def is_cliente(self):
        if self.rol.pk == 3:
            return True
        else:
            return False

    @property
    def is_fotopartner(self):
        if self.rol.pk == 3:
            fotografo = Fotografo.objects.get(pk=self.pk)
            if fotografo.fotopartner:
                return True
            else:
                return False
        else:
            return False

    @property
    def is_admin(self):
        if self.rol.pk in [2,5]:
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

class Fotografo(Usuario):
    foto_portada = models.ImageField(upload_to='foto_portada/',
                                     validators=[FileExtensionValidator(allowed_extensions=['png', 'jpg'])], null=True,
                                     blank=True)
    fotopartner = models.BooleanField(default=False)
    terminos_condiciones = models.BooleanField()
    class Meta:
        managed = True
        db_table = 'fotografo'

class SiguiendoFotografo(models.Model):
    fotografo = models.ForeignKey(Fotografo, models.DO_NOTHING, related_name='fotografo')
    siguiendo_a = models.ForeignKey(Fotografo, models.DO_NOTHING, related_name='siguiendo_a')
    class Meta:
        managed = True
        db_table = 'siguiendo_fotografo'

class Catalogo(models.Model):
    nombre = models.CharField(max_length=512)
    fecha_alta = models.DateTimeField(auto_now_add=True)
    fecha_baja = models.DateTimeField(blank=True, null=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    estatus = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre

    class Meta:
        abstract = True

class RedSocial(Catalogo):
    class Meta:
        managed = True
        db_table = 'red_social'

class UsuarioRedSocial(models.Model):
    usuario = models.ForeignKey('Usuario', models.DO_NOTHING)
    red_social = models.ForeignKey('RedSocial', models.DO_NOTHING)
    token = models.CharField(max_length=256)

    class Meta:
        managed = True
        db_table = 'usuario_has_red_social'

class Tarjeta(models.Model):
    usuario = models.ForeignKey(Usuario, models.DO_NOTHING)
    ultimos_digitos = models.CharField(max_length=5)
    token = models.CharField(max_length=64)
    alias = models.CharField(max_length=128)
    nombre_propietario = models.CharField(max_length=256)
    estatus = models.BooleanField(default=True)

    class Meta:
        managed = True
        db_table = 'tarjeta'

class BitacoraLogin(models.Model):
    usuario = models.ForeignKey(Usuario, models.DO_NOTHING)
    fecha = models.DateTimeField(auto_now_add=True)
    pass_correcto = models.BooleanField()

    class Meta:
        managed = True
        db_table = 'bitacora_login'

class Direccion(models.Model):
    usuario = models.ForeignKey(Usuario, models.DO_NOTHING)
    nombre = models.CharField(max_length=32)
    calle = models.CharField(max_length=32)
    num_exterior = models.CharField(max_length=5, null=True, blank=True)
    num_interior = models.CharField(max_length=5, null=True, blank=True)
    colonia = models.ForeignKey('Colonia', models.DO_NOTHING)
    referencias = models.TextField(max_length=512, null=True, blank=True)
    entre_calles = models.TextField(max_length=512, null=True, blank=True)
    estatus = models.BooleanField(default=True)

    class Meta:
        managed = True
        db_table = 'direccion'

    def __str__(self):
        return self.nombre

    def direccion_completa(self):
        num_ext = ('Num ext: ' + self.num_exterior) if self.num_exterior else 'S/N'
        num_int = (' Num int: ' + self.num_interior) if self.num_interior else ''
        return self.calle + ' ' + num_ext + num_int + ' CP. ' + self.colonia.cp + ' ' + self.colonia.municipio.nombre + ' ' +\
               self.colonia.municipio.estado.nombre

class Pais(Catalogo):
    class Meta:
        managed = True
        db_table = 'pais'

class Estado(Catalogo):
    pais = models.ForeignKey('Pais', on_delete=models.DO_NOTHING)

    class Meta:
        managed = True
        db_table = 'estado'

class Municipio(Catalogo):
    estado = models.ForeignKey('Estado', models.DO_NOTHING)
    cat_mun_id = models.IntegerField(null=True, blank=True)
    class Meta:
        managed = True
        db_table = 'municipio'

class Colonia(Catalogo):
    municipio = models.ForeignKey('Municipio', models.DO_NOTHING)
    cp = models.CharField(max_length=5)
    class Meta:
        managed = True
        db_table = 'colonia'

class Preferencias(models.Model):
    usuario = models.ForeignKey(Usuario, models.DO_NOTHING)

    class Meta:
        managed = True
        db_table = 'preferencias'

class Fotografia(models.Model):
    nombre = models.CharField(max_length=64)
    usuario = models.ForeignKey(Usuario, models.DO_NOTHING)
    foto_original = models.ImageField(upload_to='foto_original/', validators=[FileExtensionValidator(allowed_extensions=['png', 'jpg'])])
    foto_muestra = models.ImageField(upload_to='foto_muestra/', validators=[FileExtensionValidator(allowed_extensions=['png', 'jpg'])])
    descripcion = models.TextField(max_length=256, null=True, blank=True)
    alto = models.IntegerField()  # pixeles
    ancho = models.IntegerField()  # pixeles
    tipo_foto = models.ForeignKey("TipoFoto", models.DO_NOTHING) # Default tipo normal
    etiquetas = models.ManyToManyField('Etiqueta', related_name='fotografias_tags')
    categorias = models.ManyToManyField('Categoria', related_name='fotografias_cat')
    orientacion = models.ForeignKey("Orientacion", models.DO_NOTHING)
    tamanio = models.ForeignKey("Tamanio", models.DO_NOTHING)
    precio = models.FloatField()

    publica = models.BooleanField(default=True) # Si la foto se mostrara en la red social
    aprobada = models.BooleanField(default=False) # Si fue aprobada por un administrador
    estatus = models.BooleanField(default=True) # Si la imagen debe mostrarse o no
    fecha_alta = models.DateTimeField(auto_now_add=True)


    class Meta:
        managed = True
        db_table = 'fotografia'


class FotoReaccion(models.Model):
    usuario = models.ForeignKey(Fotografo, models.DO_NOTHING)
    foto = models.ForeignKey(Fotografia, models.DO_NOTHING)
    reaccion = models.ForeignKey("Reaccion", models.DO_NOTHING)

    class Meta:
        managed = True
        db_table = 'foto_reaccion'

class Reaccion(Catalogo):
    class Meta:
        managed = True
        db_table = 'reaccion'


class TipoFoto(Catalogo):
    precio = models.FloatField()

    class Meta:
        managed = True
        db_table = 'tipo_foto'

class Etiqueta(Catalogo):

    class Meta:
        managed = True
        db_table = 'etiqueta'

class Orientacion(Catalogo):

    class Meta:
        managed = True
        db_table = 'orientacion'

class Categoria(Catalogo):

    class Meta:
        managed = True
        db_table = 'categoria'

class Tamanio(Catalogo):

    class Meta:
        managed = True
        db_table = 'tamanio'

# TODO Eliminar modelo e importaciones
class CodigoMarco(models.Model):
    codigo = models.CharField(max_length=5, unique=True)
    estatus = models.BooleanField(default=True)

    class Meta:
        managed = True
        db_table = 'codigo_marco'

    def __str__(self):
        return self.codigo

class Marco(Catalogo):
    imagen_horizontal = models.ImageField(upload_to='img_marco/', validators=[FileExtensionValidator(allowed_extensions=['png', 'jpg'])])
    imagen_vertical = models.ImageField(upload_to='img_marco/', validators=[FileExtensionValidator(allowed_extensions=['png', 'jpg'])])
    codigo = models.CharField(max_length=5, unique=True)
    tamanio = models.ForeignKey(Tamanio, models.DO_NOTHING)
    alto = models.FloatField() # centimetros
    ancho = models.FloatField() # centimetros
    profundidad = models.FloatField() # centimetros
    peso = models.FloatField() # Kilogramos
    grosor_lado = models.FloatField()
    grosor_total = models.FloatField()
    grosor_final = models.FloatField()
    precio = models.FloatField()

    class Meta:
        managed = True
        db_table = 'marco'

class ModeloMariaLuisa(models.Model):

    fecha_alta = models.DateTimeField(auto_now_add=True)
    fecha_baja = models.DateTimeField(blank=True, null=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    estatus = models.BooleanField(default=True)
    modelo = models.CharField(max_length=6, unique=True)

    class Meta:
        managed = True
        db_table = 'modelo_maria_luisa'

    def __str__(self):
        return self.modelo

class MariaLuisa(Catalogo):
    imagen = models.ImageField(upload_to='img_marialuisa/',
                               validators=[FileExtensionValidator(allowed_extensions=['png', 'jpg'])])
    modelo = models.ForeignKey(ModeloMariaLuisa, models.DO_NOTHING)
    precio = models.FloatField()
    tamanio = models.ForeignKey(Tamanio, models.DO_NOTHING)
    alto = models.FloatField()  # centimetros
    ancho = models.FloatField()  # centimetros

    class Meta:
        managed = True
        db_table = 'maria_luisa'


class TipoPapel(Catalogo):

    class Meta:
        managed = True
        db_table = 'tipo_papel'

class PapelImpresion(models.Model):
    tipo_papel = models.ForeignKey('TipoPapel', models.DO_NOTHING)
    tamanio = models.ForeignKey('Tamanio', models.DO_NOTHING)
    precio = models.FloatField()
    estatus = models.BooleanField(default=True)

    class Meta:
        managed = True
        db_table = 'papel_impresion'


    def __str__(self):
        return self.tipo_papel.nombre + ' ' + self.tamanio.nombre

class FotoPrecio(models.Model):
    tamanio = models.ForeignKey('Tamanio', models.DO_NOTHING)
    precio = models.FloatField()
    estatus = models.BooleanField(default=True)

    class Meta:
        managed = True
        db_table = 'foto_precio'


    def __str__(self):
        return self.tipo_papel.nombre + ' ' + self.tamanio.nombre

class Textura(Catalogo):
    imagen = models.ImageField(upload_to='img_texturas/',
                               validators=[FileExtensionValidator(allowed_extensions=['png', 'jpg'])])
    class Meta:
        managed = True
        db_table = 'textura'

class Logo(Catalogo):
    imagen = models.ImageField(upload_to='logo/',
                               validators=[FileExtensionValidator(allowed_extensions=['png', 'jpg'])])
    class Meta:
        managed = True
        db_table = 'logo'

class MenuFotopartner(Catalogo):
    url = models.CharField(max_length=256)
    class Meta:
        managed = True
        db_table = 'menu_fotopartner'

class FormaPago(Catalogo):
    porcentaje_comision = models.FloatField(validators=[MinValueValidator(0.0), MaxValueValidator(100)])

    class Meta:
        managed = True
        db_table = 'forma_pago'

class EstatusPago(Catalogo):
    class Meta:
        managed = True
        db_table = 'estatus_pago'

class TipoCompra(Catalogo):
    class Meta:
        managed = True
        db_table = 'tipo_compra'

class DimensionOrden(models.Model):
    orden = models.OneToOneField('Orden', models.DO_NOTHING)
    alto = models.FloatField() # centimetros
    ancho = models.FloatField() # centimetros
    profundidad = models.FloatField() # centimetros

    class Meta:
        managed = True
        db_table = 'dimension_orden'

class TipoComision(Catalogo):

    class Meta:
        managed = True
        db_table = 'tipo_comision'

class Comision(Catalogo):
    porcentaje_comision = models.FloatField(validators=[MinValueValidator(0.0), MaxValueValidator(100)])

    class Meta:
        managed = True
        db_table = 'comision'

class Orden(models.Model):
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_compra = models.DateField(null=True, blank=True)
    usuario = models.ForeignKey('Usuario', models.DO_NOTHING)
    direccion = models.ForeignKey('Direccion', models.DO_NOTHING)
    tarjeta = models.ForeignKey('Tarjeta', models.DO_NOTHING, null=True, blank=True)
    oxxo_order = models.CharField(max_length=12)
    num_guia = models.CharField(max_length=12, null=True, blank=True)
    peso = models.FloatField(default=0)
    costo_envio = models.FloatField()
    forma_pago = models.ForeignKey('FormaPago', models.DO_NOTHING)
    comision = models.ForeignKey('Comision', models.DO_NOTHING, null=True, blank=True)
    promocion = models.ForeignKey('Promocion', models.DO_NOTHING, null=True, blank=True)
    estatus = models.ForeignKey('EstatusPago', models.DO_NOTHING)
    order_id = models.CharField(max_length=512, blank=True, null=True)
    total = models.FloatField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'orden'

class Producto(models.Model):
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    usuario = models.ForeignKey(Usuario, models.DO_NOTHING)
    orden = models.ForeignKey('Orden', models.CASCADE, related_name='productos')
    foto = models.ForeignKey(Fotografia, models.DO_NOTHING)
    marco = models.ForeignKey(Marco, models.DO_NOTHING, null=True, blank=True)
    maria_luisa = models.ForeignKey(MariaLuisa, models.DO_NOTHING, null=True, blank=True)
    tipo_compra = models.ForeignKey(TipoCompra, models.DO_NOTHING)
    papel_impresion = models.ForeignKey('PapelImpresion', models.DO_NOTHING, null=True, blank=True)
    promocion_aplicada = models.ForeignKey('Promocion', models.DO_NOTHING, null=True, blank=True)
    estatus_pago_fotografo = models.ForeignKey(EstatusPago, models.DO_NOTHING)

    class Meta:
        managed = True
        db_table = 'producto'

class Descarga(models.Model):
    producto = models.ForeignKey('Producto', models.DO_NOTHING)
    token = models.CharField(max_length=64)
    no_descargas_disponibles = models.PositiveIntegerField(default=3)

    class Meta:
        managed = True
        db_table = 'descarga'


class TipoPromocion(Catalogo):

    class Meta:
        managed = True
        db_table = 'tipo_promocion'

class Promocion(models.Model):
    nombre = models.CharField(max_length=256)
    total_cupones = models.PositiveIntegerField()
    usos_por_usuario = models.PositiveIntegerField()
    codigo_promocion = models.CharField(max_length=8, unique=True)
    fecha_inicio = models.DateTimeField()
    fecha_fin = models.DateTimeField()
    tipo_promocion = models.ForeignKey('TipoPromocion', models.DO_NOTHING)
    porcentaje_cantidad = models.FloatField()
    tipo_compra = models.ForeignKey('TipoCompra', models.DO_NOTHING)
    marco = models.ForeignKey('Marco', models.DO_NOTHING, null=True, blank=True)
    tamanio_marco = models.ForeignKey('Tamanio', models.DO_NOTHING, null=True, blank=True)
    maria_luisa = models.ForeignKey('MariaLuisa', models.DO_NOTHING, null=True, blank=True)
    imagen = models.ImageField(upload_to='promo_fotoferta/', validators=[FileExtensionValidator(allowed_extensions=['png', 'jpg'])], null=True, blank=True)
    forma_pago = models.ForeignKey('FormaPago', models.DO_NOTHING, null=True, blank=True)
    estatus = models.BooleanField(default=True)
    class Meta:
        managed = True
        db_table = 'promocion'

class PersonalAdministrativo(Usuario):

    class Meta:
        managed = True
        db_table = 'personal_administrativo'


class Contactanos(models.Model):
    direccion = models.TextField(max_length=256)
    telefono = models.CharField(max_length=12)
    correo = models.EmailField(max_length=32)


    class Meta:
        managed = True
        db_table = 'contactanos'