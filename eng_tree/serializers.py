from rest_framework import serializers


class ParaphraseSerializer(serializers.Serializer):
    tree = serializers.CharField()
