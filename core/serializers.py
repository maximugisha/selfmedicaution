from rest_framework import serializers


class SymptomSerializer(serializers.Serializer):
    symptoms = serializers.CharField(max_length=200)