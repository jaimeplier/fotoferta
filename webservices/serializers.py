from rest_framework import serializers

from config.models import Contactanos


class ContactanosSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contactanos
        fields = '__all__'