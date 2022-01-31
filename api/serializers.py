from rest_framework import serializers
from locos.models import Builder

class BuilderSerializer(serializers.ModelSerializer):

    class Meta:
        model = Builder
        fields = ['id', 'name', 'wikislug']