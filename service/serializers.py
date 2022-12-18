from rest_framework import serializers


class ServiceSerializer(serializers.Serializer):
    title = serializers.CharField(read_only=True)
    price = serializers.IntegerField(read_only=True)


class CategorySerializer(serializers.Serializer):
    title = serializers.CharField(read_only=True)
    services = ServiceSerializer(many=True)
