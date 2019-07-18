from rest_framework import serializers

from config.models import Contactanos, Fotografia, Categoria, Etiqueta


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
