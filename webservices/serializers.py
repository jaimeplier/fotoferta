from rest_framework import serializers

from config.models import Contactanos, Fotografia, Categoria, Etiqueta, TipoCompra, Producto, Orden, Direccion, Tarjeta, \
    FormaPago, Marco, PapelImpresion


class ContactanosSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contactanos
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
    #publica = serializers.BooleanField()
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


class OrdenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Orden
        fields = ['direccion', 'tarjeta', 'oxxo_order', 'num_guia', 'peso', 'costo_envio', 'forma_pago', 'comision',
                  'promocion', 'estatus', 'estatus_compra', 'order_id', 'total']

class FotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Fotografia
        fields = ['nombre', 'descripcion', 'tamanio', 'foto_muestra']

class TipoCompraSerializer(serializers.ModelSerializer):
    class Meta:
        model = TipoCompra
        fields = ['nombre']

class ProductoSerializer(serializers.ModelSerializer):
    foto = FotoSerializer()
    tipo_compra = TipoCompra()
    class Meta:
        model = Producto
        fields = ['pk', 'usuario', 'orden', 'foto', 'marco', 'maria_luisa', 'tipo_compra', 'papel_impresion',
                  'promocion_aplicada', 'subtotal']

class MarcoSerializer(serializers.ModelSerializer):

    class Meta:
        model = Marco
        fields = '__all__'

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
        fields = ['pk', 'usuario', 'alias', 'terminacion', 'nombre_propietario']

class PagarOrdenSerializer(serializers.Serializer):
    orden = serializers.IntegerField()
    metodo_pago = serializers.IntegerField()
    direccion = serializers.IntegerField()
    tarjeta = serializers.IntegerField(allow_null=True, required=False)

    def validate_orden(self, value):
        try:
            orden = Orden.objects.get(pk=value)
            orden_usuario = Orden.objects.filter(pk=orden.pk, usuario=self.request.user)
            if len(orden_usuario)<=0:
                raise serializers.ValidationError('No es posible pagar la orden de pago seleccionada')
        except:
            raise serializers.ValidationError('No existe el producto seleccionado')
        return value

    def validate_metodo_pago(self, value):
        try:
            FormaPago.objects.get(pk=value)
        except:
            raise serializers.ValidationError('No existe el método de pago seleccionado')
        return value

    def validate_tarjeta(self, value):
        try:
            forma_pago = FormaPago.objects.get(pk=value)
            if forma_pago.nombre == 'Tarjeta':
                try:
                    Tarjeta.objects.get(pk=value)
                    tarjeta_usuario = Tarjeta.objects.filter(pk=value, usuario=self.request.user)
                    if tarjeta_usuario <=0:
                        raise serializers.ValidationError('Debes seleccionar una tarjeta')
                except:
                    raise serializers.ValidationError('Debes seleccionar una tarjeta')

        except:
            raise serializers.ValidationError('No existe el método de pago seleccionado')
        return value

    def validate_direccion(self, value):
        try:
            direccion=Direccion.objects.get(pk=value)
            direccion_usuario = Direccion.objects.filter(pk=direccion.pk, usuario=self.request.user)
            if len(direccion_usuario) <= 0:
                raise serializers.ValidationError('No es posible elegir la dirección seleccionada')
        except:
            raise serializers.ValidationError('No existe el método de pago seleccionado')
        return value