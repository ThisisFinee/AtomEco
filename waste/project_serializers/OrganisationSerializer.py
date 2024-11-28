from waste.project_serializers.BaseSerializer import BaseSerializer
from waste.models import Organization


class OrganizationSerializer(BaseSerializer):

    class Meta:
        model = Organization
        fields = '__all__'

    def create(self, validated_data):
        allowed_keys = ['relations', 'name', 'generate_plastic', 'generate_glass', 'generate_bio_wastes']
        validated_data = self.filter_validated_data(validated_data, allowed_keys)
        instance = super().create(validated_data)
        self.structure_regenerate(instance)
        return instance

    def update(self, instance, validated_data):
        allowed_keys = ['name', 'generate_plastic', 'generate_glass', 'generate_bio_wastes']
        validated_data = self.filter_validated_data(validated_data, allowed_keys)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        self.post_save_actions(instance)
        return instance

