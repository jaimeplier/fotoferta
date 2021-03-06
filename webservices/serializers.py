from rest_framework import serializers

from config.models import Contactanos, Fotografia, Categoria, Etiqueta, TipoCompra, Producto, Orden, Direccion, Tarjeta, \
    FormaPago, Marco, PapelImpresion, Tamanio, TipoPapel, Textura, FotoPrecio, MariaLuisa, Pais, Estado, Municipio, \
    Colonia, FotoReaccion, SiguiendoFotografo, Fotografo, RedSocial, Logo, MotivoReporte, Promocion, Notificacion, \
    Reaccion


class ContactanosSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contactanos
        fields = '__all__'

class LogoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Logo
        fields = ['imagen']

class RedSocialSerializer(serializers.ModelSerializer):
    class Meta:
        model = RedSocial
        fields = '__all__'

class CategoriasSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = ['pk', 'nombre']

class EtiquetaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = ['pk', 'nombre']

class TagsSerializer(serializers.Serializer):
    pk = serializers.IntegerField()

    def validate_pk(self, value):
        try:
            Etiqueta.objects.get(pk=value)
        except:
            raise serializers.ValidationError('El ID: '+str(value)+ 'de etiqueta no existe')
        return value

class RegistroFotografiaSerializer(serializers.Serializer):
    foto = serializers.ImageField()
    tipo_venta_foto = serializers.IntegerField(min_value=1, max_value=3)
    publica = serializers.BooleanField()
    categoria = serializers.CharField(max_length=100)
    nombre = serializers.CharField(max_length=64)
    descripcion = serializers.CharField(max_length=256)
    etiquetas = serializers.CharField(max_length=100)

    def validate_foto(self, value):
        if value.size > 25000000:
            raise serializers.ValidationError('La foto debe ser menor a 25MB')
        return value


class FotografiaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Fotografia
        fields = ['pk',
                  'nombre',
                  'usuario',
                  'foto_muestra',
                  'foto_home',
                  'descripcion',
                  'tipo_foto',
                  'etiquetas',
                  'categorias',
                  'tamanio',
                  'precio']

class AddFotoCarritoSerializer(serializers.Serializer):
    pk = serializers.IntegerField()
    tipo_compra = serializers.IntegerField()

    def validate_pk(self, value):
        try:
            Fotografia.objects.get(pk=value)
        except:
            raise serializers.ValidationError('No existe la foto seleccionada')
        return value

    def validate_tipo_compra(self, value):
        try:
            TipoCompra.objects.get(pk=value)
        except:
            raise serializers.ValidationError('No existe el tipo de compra seleccionado')
        return value

class EditProductoSerializer(serializers.Serializer):
    producto = serializers.IntegerField()
    precio_tamanio = serializers.IntegerField()
    marco = serializers.IntegerField()
    papel_impresion = serializers.IntegerField()
    maria_luisa = serializers.IntegerField(allow_null=True, required=False)

    def validate_pk(self, value):
        try:
            prod = Producto.objects.get(pk=value)
            if prod.usuario != self.request.user:
                raise serializers.ValidationError('No puedes modificar éste producto')
        except:
            raise serializers.ValidationError('No existe el producto seleccionado')
        return value

    def validate_marco(self, value):
        try:
            Marco.objects.get(pk=value, estatus=True)
        except:
            raise serializers.ValidationError('No existe el marco seleccionado')
        return value

    def validate_papel_impresion(self, value):
        try:
            PapelImpresion.objects.get(pk=value, estatus=True)
        except:
            raise serializers.ValidationError('No existe el papel seleccionado')
        return value

    def validate_precio_tamanio(self, value):
        try:
            FotoPrecio.objects.get(pk=value, estatus=True)
        except:
            raise serializers.ValidationError('No existe el tamaño seleccionado')
        return value


class OrdenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Orden
        fields = ['direccion', 'tarjeta', 'oxxo_order', 'num_guia', 'peso', 'costo_envio', 'forma_pago', 'comision',
                  'promocion', 'estatus', 'estatus_compra', 'order_id', 'total']

class FotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Fotografia
        fields = ['pk', 'nombre', 'descripcion', 'tamanio', 'foto_muestra']

class ReaccionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reaccion
        fields = ['nombre']

class FotoReaccionSerializer(serializers.ModelSerializer):
    foto = FotografiaSerializer()
    class Meta:
        model = FotoReaccion
        fields = ['foto', 'usuario', 'reaccion']

class FotografoSerializer(serializers.ModelSerializer):

    class Meta:
        model = Fotografo
        fields = ['id', 'foto_perfil', 'nombre', 'correo', 'seguidores']

class NotificacionSerializer(serializers.ModelSerializer):
    reaccion = ReaccionSerializer()
    actioner = FotografoSerializer()
    receiver = FotografoSerializer()
    foto = FotoSerializer()
    class Meta:
        model = Notificacion
        fields = ['actioner', 'reaccion', 'receiver', 'foto']

class FotoparterSiguiendoSerializer(serializers.ModelSerializer):
    siguiendo_a = FotografoSerializer()
    class Meta:
        model = SiguiendoFotografo
        fields = ['siguiendo_a']

class TipoCompraSerializer(serializers.ModelSerializer):
    class Meta:
        model = TipoCompra
        fields = ['nombre']

class MarcoSerializer(serializers.ModelSerializer):

    class Meta:
        model = Marco
        fields = '__all__'

class MariaLuisaSerializer(serializers.ModelSerializer):

    class Meta:
        model = MariaLuisa
        fields = '__all__'

class TamanioSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tamanio
        fields = ['pk', 'nombre']

class FotoPrecioSerializer(serializers.ModelSerializer):
    tamanio = TamanioSerializer()

    class Meta:
        model = FotoPrecio
        fields = ['pk', 'tamanio', 'precio']

class TipoPapelSerializer(serializers.ModelSerializer):

    class Meta:
        model = TipoPapel
        fields = ['pk', 'nombre']

class PapelImpresionSerializer(serializers.ModelSerializer):
    tipo_papel =TipoPapelSerializer()
    class Meta:
        model = PapelImpresion
        fields = ['pk', 'tipo_papel', 'precio']

class TexturaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Textura
        fields = ['pk', 'nombre', 'imagen']

class ProductoPKSerializer(serializers.Serializer):
    pk = serializers.IntegerField()

    def validate_pk(self, value):
        try:
            Producto.objects.get(pk=value)
        except:
            raise serializers.ValidationError('No existe el producto seleccionado')
        return value

class DireccionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Direccion
        fields = ['pk', 'usuario', 'nombre', 'calle', 'num_exterior', 'num_interior', 'colonia', 'referencias',
                  'entre_calles']

class TarjetaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tarjeta
        fields = ['pk', 'usuario', 'alias', 'ultimos_digitos', 'nombre_propietario']

class PagarOrdenSerializer(serializers.Serializer):
    #orden = serializers.IntegerField()
    metodo_pago = serializers.IntegerField()
    direccion = serializers.IntegerField(allow_null=True, required=False)
    tarjeta = serializers.IntegerField(allow_null=True, required=False)

    # def validate_orden(self, value):
    #     try:
    #         orden = Orden.objects.get(pk=value)
    #         orden_usuario = Orden.objects.filter(pk=orden.pk, usuario=self.request.user)
    #         if len(orden_usuario)<=0:
    #             raise serializers.ValidationError('No es posible pagar la orden seleccionada')
    #     except:
    #         raise serializers.ValidationError('No existe el producto seleccionado')
    #     return value
    #
    # def validate_metodo_pago(self, value):
    #     try:
    #         FormaPago.objects.get(pk=value)
    #     except:
    #         raise serializers.ValidationError('No existe el método de pago seleccionado')
    #     return value
    #
    # def validate_tarjeta(self, value):
    #     try:
    #         forma_pago = FormaPago.objects.get(pk=self.metodo_pago)
    #         if forma_pago.nombre == 'Tarjeta':
    #             try:
    #                 Tarjeta.objects.get(pk=value)
    #                 tarjeta_usuario = Tarjeta.objects.filter(pk=value, usuario=self.request.user)
    #                 if tarjeta_usuario <=0:
    #                     raise serializers.ValidationError('Debes seleccionar una tarjeta')
    #             except:
    #                 raise serializers.ValidationError('Debes seleccionar una tarjeta')
    #
    #     except:
    #         raise serializers.ValidationError('No existe el método de pago seleccionado')
    #     return value
    #
    # def validate_direccion(self, value):
    #     try:
    #         orden = Orden.objects.get(pk=self.orden)
    #         num_productos = Producto.objects.filter(orden =orden, tipo_compra__pk=2).count()
    #         if num_productos == 0: # No requiere direccion, todos son digitales
    #             return value
    #         direccion=Direccion.objects.get(pk=value)
    #         direccion_usuario = Direccion.objects.filter(pk=direccion.pk, usuario=self.request.user)
    #         if len(direccion_usuario) <= 0:
    #             raise serializers.ValidationError('No es posible elegir la dirección seleccionada')
    #     except:
    #         raise serializers.ValidationError('No existe el método de pago seleccionado')
    #     return value


class ProductoSerializer(serializers.ModelSerializer):
    foto = FotoSerializer()
    tipo_compra = TipoCompra()
    marco = MarcoSerializer()
    maria_luisa = MariaLuisaSerializer()
    papel_impresion = PapelImpresionSerializer()

    class Meta:
        model = Producto
        fields = ['pk', 'usuario', 'orden', 'foto', 'marco', 'maria_luisa', 'tipo_compra', 'papel_impresion',
                  'promocion_aplicada', 'subtotal']

class PaisSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pais
        fields = ['pk', 'nombre']

class EstadoSerializer(serializers.ModelSerializer):
    pais = PaisSerializer()
    class Meta:
        model = Estado
        fields = ['pk', 'nombre', 'pais']

class MunicipioSerializer(serializers.ModelSerializer):
    estado = EstadoSerializer()
    class Meta:
        model = Municipio
        fields = ['pk', 'nombre', 'estado']

class ColoniaSerializer(serializers.ModelSerializer):
    municipio = MunicipioSerializer()
    class Meta:
        model = Colonia
        fields = ['pk', 'nombre', 'municipio']

class AddFavoritoSerializer(serializers.Serializer):
    foto= serializers.IntegerField()
    like = serializers.BooleanField()

    def validate_foto(self, value):
        try:
            Fotografia.objects.get(pk=value)
        except:
            raise serializers.ValidationError('No existe la fotografía seleccionada')
        return value

class AddSeguidorSerializer(serializers.Serializer):
    fotopartner= serializers.IntegerField()
    seguir = serializers.BooleanField()

    def validate_fotopartner(self, value):
        try:
            Fotografo.objects.get(pk=value)
        except:
            raise serializers.ValidationError('No existe el fotoparter seleccionado')
        return value

class LoginSerializer(serializers.Serializer):
    correo = serializers.EmailField()
    token = serializers.CharField(max_length=256)
    red_social = serializers.IntegerField()

class FotoPerfilSerializer(serializers.Serializer):
    foto = serializers.ImageField()

class FotoPortadaSerializer(serializers.Serializer):
    foto = serializers.ImageField()

class RegistroRedesSerializer(serializers.Serializer):
    nombre = serializers.CharField(max_length=64)
    correo = serializers.EmailField()
    red_social = serializers.IntegerField()
    token = serializers.CharField(max_length=256)

class ReporteFotoSerializer(serializers.Serializer):
    foto = serializers.IntegerField()
    motivo_reporte = serializers.IntegerField()
    descripcion = serializers.CharField(max_length=1024)

    def validate_foto(self, value):
        try:
            Fotografia.objects.get(pk=value)
        except:
            raise serializers.ValidationError('No existe la foto seleccionada')
        return value

    def validate_motivo_reporte(self, value):
        try:
            MotivoReporte.objects.get(pk=value)
        except:
            raise serializers.ValidationError('No existe el motivo de reporte')
        return value

class PromocionBannerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Promocion
        fields = ['pk', 'nombre', 'imagen']