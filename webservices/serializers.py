from rest_framework import serializers


class EstatusSerializer(serializers.Serializer):
    pk = serializers.IntegerField()