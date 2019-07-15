from rest_framework import serializers

from config.models import Contactanos, Fotografia, Categoria


class ContactanosSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contactanos
        fields = '__all__'

class CategoriasSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = ['pk', 'nombre']

class RegistroFotografiaSerializer(serializers.Serializer):
    tipo_foto = serializers.IntegerField(min_value=0, max_value=3)
    categoria = serializers.IntegerField(min_value=0)