from rest_framework import serializers
from people.models import Person
from companies.models import Manufacturer

def name_length(value):
    if len(value) < 2:
        raise serializers.ValidationError("Name is too short!")

class ManufacturerSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(validators=[name_length])
    wikislug = serializers.CharField()

    def create(self, validated_data):
        return Manufacturer.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.wikislug = validated_data.get('wikislug', instance.wikislug)
        instance.save()
        return instance

    def validate(self, data):
        if data['name'] == data['wikislug']:
            raise serializers.ValidationError("Name and wikislug should be different!")
        else:
            return data

    def validate_name(self, value):
        if len(value) < 2:
            raise serializers.ValidationError("Name is too short!")
        else:
            return value


class PersonSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(validators=[name_length])
    birthdate = serializers.CharField()
    dieddate = serializers.CharField()

    def create(self, validated_data):
        return Person.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.birthdate = validated_data.get('birthdate', instance.birthdate)
        instance.dieddate = validated_data.get('dieddate', instance.dieddate)
        instance.save()
        return instance

    def validate_name(self, value):
        if len(value) < 2:
            raise serializers.ValidationError("Name is too short!")
        else:
            return value