from waste.project_serializers.BaseSerializer import BaseSerializer
from waste.models import Connection


class ConnectionSerializer(BaseSerializer):
    class Meta:
        model = Connection
        fields = '__all__'

    def create(self, validated_data):
        allowed_keys = ['relations', 'first_point', 'second_point', 'distance']
        validated_data = self.filter_validated_data(validated_data, allowed_keys)
        instance = super().create(validated_data)
        self.post_save_actions(instance)
        return instance

    def update(self, instance, validated_data):
        allowed_keys = ['distance']
        validated_data = self.filter_validated_data(validated_data, allowed_keys)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        self.post_save_actions(instance)
        return instance
