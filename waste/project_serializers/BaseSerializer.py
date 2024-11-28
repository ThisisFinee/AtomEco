from rest_framework import serializers
from waste.workfiles.Navigator import Navigator
from waste.workfiles.GraphConstructor import GraphConstructor


class BaseSerializer(serializers.ModelSerializer):

    def filter_validated_data(self, validated_data, allowed_keys):
        return {key: validated_data[key] for key in allowed_keys if key in validated_data}

    def post_save_actions(self, instance):
        GraphConstructor.generate_graph_structure(instance.relations)
        Navigator.recalculate_all_paths(instance.relations)

    def structure_regenerate(self, instance):
        GraphConstructor.generate_graph_structure(instance.relations)