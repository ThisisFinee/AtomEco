from rest_framework import viewsets, status
from waste.models import Relations
from waste.serializers import RelationsSerializer
from rest_framework.decorators import action
from waste.workfiles.Navigator import Navigator
from rest_framework.response import Response


class RelationsView(viewsets.ModelViewSet):
    queryset = Relations.objects.all()
    serializer_class = RelationsSerializer

    @action(detail=True, methods=['patch'])
    def recalculate_paths(self, request, pk=None):
        try:
            relations = self.get_object()
            Navigator.recalculate_all_paths(relations)
            relations_serialized = RelationsSerializer(relations).data
            return Response({"message": f"Paths recalculated successfully for relations with id: {relations.id}",
                             "relations": relations_serialized}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['patch'])
    def generate_graph_structure(self, request, pk=None):
        from ..workfiles.GraphConstructor import GraphConstructor
        try:
            relations = self.get_object()
            GraphConstructor.generate_graph_structure(relations)
            relations_serialized = RelationsSerializer(relations).data
            return Response({"message": f"Graph structure generated successfully for relations with id: {relations.id}",
                             "relations": relations_serialized}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'])
    def generate_graph(self, request):
        from ..workfiles.Generator import Generator

        graph_type = request.query_params.get('type')
        if not graph_type:
            return Response({"error": "Parameter 'type' is required."}, status=400)

        if graph_type == 'base':
            relations = Generator.generate_test_graph()
        elif graph_type == 'spec':
            relations = Generator.generate_specific_graph()
        elif graph_type == 'intersection':
            relations = Generator.generate_graph_with_intersections()
        elif graph_type == 'error':
            relations = Generator.generate_error_graph()
        else:
            return Response({"error": f"Unknown graph type: {graph_type}"}, status=400)

        relations_serialized = RelationsSerializer(relations).data

        return Response({"message": f"Graph of type '{graph_type}' generated successfully.",
                         "relations": relations_serialized}, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['post'])
    def generate_random_graphs(self, request):
        from ..workfiles.Generator import Generator

        graphs_type = request.query_params.get('type')
        graphs_number = int(request.query_params.get('number', 5))
        if not graphs_type:
            return Response({"error": "Parameter 'type' is required."}, status=400)

        if graphs_type == 'full':
            relations_array = Generator.generate_fully_graphs(graphs_number)
        elif graphs_type == 'partial':
            relations_array = Generator.generate_partially_graphs(graphs_number)
        else:
            return Response({"error": f"Unknown graph type: {graphs_type}"}, status=400)
        relations_array_serialized = RelationsSerializer(relations_array, many=True).data

        return Response({"message": f"Graphs of type '{graphs_type}', graphs number: {graphs_number},"
                                    f" generated successfully.",
                         "all_generate_relations": [rel for rel in relations_array_serialized]},
                        status=status.HTTP_201_CREATED)
