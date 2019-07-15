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
    tipo_foto = serializers.IntegerField(min_value=0, max_value=3)
    categoria = serializers.IntegerField(min_value=0)
    nombre = serializers.CharField(max_length=64)
    etiquetas = serializers.ListField(child=TagsSerializer(), required=True)