from rest_framework import serializers

from config.models import Contactanos, Fotografia, Categoria, Etiqueta, TipoCompra, Producto, Orden


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
    categoria = serializers.IntegerField(min_value=0)
    nombre = serializers.CharField(max_length=64)
    descripcion = serializers.CharField(max_length=256)
    etiquetas = serializers.CharField(max_length=100)

    def validate_categoria(self, value):
        try:
            Categoria.objects.get(pk=value)
        except:
            raise serializers.ValidationError('No existe la categoría seleccionada')
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

class OrdenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Orden
        fields = ['direccion', 'tarjeta', 'oxxo_order', 'num_guia', 'peso', 'costo_envio', 'forma_pago', 'comision',
                  'promocion', 'estatus', 'estatus_compra', 'order_id', 'total']

class FotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Fotografia
        fields = ['nombre', 'descripcion', 'tamanio']

class TipoCompraSerializer(serializers.ModelSerializer):
    class Meta:
        model = TipoCompra
        fields = ['nombre']

class ProductoSerializer(serializers.ModelSerializer):
    foto = FotoSerializer()
    tipo_compra = TipoCompra()
    class Meta:
        model = Producto
        fields = ['usuario', 'orden', 'foto', 'marco', 'maria_luisa', 'tipo_compra', 'papel_impresion',
                  'promocion_aplicada', 'subtotal']

class ProductoPKSerializer(serializers.Serializer):
    pk = serializers.IntegerField()

    def validate_pk(self, value):
        try:
            Producto.objects.get(pk=value)
        except:
            raise serializers.ValidationError('No existe el producto seleccionado')
        return value