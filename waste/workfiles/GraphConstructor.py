class GraphConstructor:

    @staticmethod
    def generate_graph_structure(relations):
        from waste.models import Organization, WasteStorage, Connection
        graph_structure = {
            "nodes": [],
            "edges": []
        }

        organizations = Organization.objects.filter(relations=relations)
        storages = WasteStorage.objects.filter(relations=relations)

        # Добавляем организации в nodes
        for org in organizations:
            graph_structure["nodes"].append({
                "id": org.id,
                "type": "Organization",
                "name": org.name
            })

        # Добавляем хранилища в nodes
        for storage in storages:
            graph_structure["nodes"].append({
                "id": storage.id,
                "type": "WasteStorage",
                "name": storage.name
            })

        # Получение всех соединений, связанных с данным Relations
        connections = Connection.objects.filter(relations=relations)

        # Добавляем соединения в edges
        for connection in connections:
            graph_structure["edges"].append({
                "from": connection.first_point.id,
                "to": connection.second_point.id,
                "distance": connection.distance,
                "id": connection.id
            })

        # Сохраняем graph_structure в Relations
        relations.graph_structure = graph_structure
        relations.save()

        return graph_structure
