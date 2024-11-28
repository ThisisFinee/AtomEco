from rest_framework import serializers
from waste.models import Relations


class RelationsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Relations
        fields = '__all__'

    def update(self, instance, validated_data):
        if 'relations_name' in validated_data:
            setattr(instance, 'relations_name', validated_data['relations_name'])
        instance.save()
        return instance
