from waste.project_serializers.BaseSerializer import BaseSerializer
from waste.models import WasteStorage
from rest_framework import serializers


class WasteStorageSerializer(BaseSerializer):

    class Meta:
        model = WasteStorage
        fields = '__all__'

    def create(self, validated_data):
        allowed_keys = ['relations', 'name', 'max_plastic', 'max_glass', 'max_bio_wastes']
        validated_data = self.filter_validated_data(validated_data, allowed_keys)
        instance = super().create(validated_data)
        self.structure_regenerate(instance)
        return instance

    def update(self, instance, validated_data):
        allowed_keys = ['name', 'max_plastic', 'max_glass', 'max_bio_wastes']
        validated_data = self.filter_validated_data(validated_data, allowed_keys)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        self.post_save_actions(instance)
        return instance

