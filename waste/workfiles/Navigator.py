from collections import defaultdict, deque
from waste.workfiles.StateReturner import StateReturner


class Navigator:

    @staticmethod
    def calculate_path_for_organization(organization):
        from waste.models import Relations, WasteStorage
        from django.db import transaction

        relations = Relations.objects.filter(basepoint=organization).first()
        if not relations or not relations.graph_structure:
            return

        graph = relations.graph_structure
        edges = graph['edges']

        remaining_wastes = {
            "plastic": organization.plastic or 0,
            "glass": organization.glass or 0,
            "bio_wastes": organization.bio_wastes or 0,
        }

        paths = []
        result_path = []
        result_distance = 0
        used_edges = set()
        visited_nodes = set()

        def clean_useless_paths():
            delete_distance = 0
            while paths and all(amount == 0 for amount in paths[-1]['waste_distribution'].values()):
                result_path.pop()
                delete_distance = paths[-1]['distance']
                paths.pop()
            return delete_distance

        def find_shortest_edge(from_node, exclude_edges=None):
            exclude_edges = exclude_edges or set()
            available_edges = [
                edge for edge in edges
                if edge['from'] == from_node and edge['id'] not in used_edges and edge['id'] not in exclude_edges
            ]
            return min(available_edges, key=lambda e: e['distance'], default=None)

        current_node = organization.id
        backtrack_stack = []  # Для возврата к последнему перекрёстку
        exclude_edges = set()  # Исключаемые рёбра при возвратах

        while any(amount > 0 for amount in remaining_wastes.values()):  # Пока есть отходы
            edge = find_shortest_edge(current_node, exclude_edges)
            if not edge:  # Если тупик
                if backtrack_stack:  # Возвращаемся к последнему перекрёстку
                    backtrack_node, used_path = backtrack_stack.pop()

                    # Освобождаем текущее ребро для повторного использования
                    exclude_edges.discard(used_path[1])

                    edge_distance = next(edge['distance'] for edge in edges if edge['id'] == used_path[1])
                    paths.append({
                        "path": used_path,
                        "distance": edge_distance,
                        "waste_distribution": {waste: 0 for waste in remaining_wastes}
                    })
                    result_path.extend(used_path)
                    result_distance += edge_distance
                    current_node = backtrack_node
                    result_distance -= clean_useless_paths()
                    continue
                else:
                    break  # Все пути исследованы

            # Переход к следующему узлу
            target_node = edge['to']
            storage = WasteStorage.objects.filter(id=target_node).first()
            if not storage:
                continue

            # Распределение отходов
            waste_distribution = {}
            for waste_type, amount in remaining_wastes.items():
                waste_distribution[waste_type] = 0
                if amount > 0:
                    max_capacity = getattr(storage, f"max_{waste_type}", 0)
                    current_storage = getattr(storage, waste_type, 0)
                    available_capacity = max_capacity - current_storage

                    if available_capacity > 0:
                        to_store = min(amount, available_capacity)
                        waste_distribution[waste_type] = to_store
                        remaining_wastes[waste_type] -= to_store
                        # Изменяем данные объектов в бд
                        setattr(storage, waste_type, current_storage + to_store)
                        storage.save()
                        setattr(organization, waste_type, remaining_wastes[waste_type])
                        organization.save()

            used_edges.add(edge['id'])

            path_segment = [[current_node, target_node], edge['id']]
            paths.append({
                "path": path_segment,
                "distance": edge['distance'],
                "waste_distribution": waste_distribution
            })
            result_path.append([current_node, target_node])
            result_distance += edge['distance']

            # Сохраняем текущее состояние для возврата при тупике
            if len([e for e in edges if e['from'] == current_node]) > 1:
                backtrack_stack.append((current_node, path_segment))
            else:
                exclude_edges.add(edge['id'])  # Исключить путь только если он полностью исследован

            current_node = target_node
            visited_nodes.add(current_node)

        # Проверка оставшихся отходов
        error = any(amount > 0 for amount in remaining_wastes.values())

        # Сохранение результатов
        with transaction.atomic():
            relations.ways_structure = relations.ways_structure or {}
            relations.ways_structure[organization.id] = {
                "error": error,
                "paths": paths,
                "result_path": result_path,
                "result_distance": result_distance
            }
            relations.save()

    @staticmethod
    def recalculate_all_paths(relations):
        from waste.models import Organization
        from waste.workfiles.GraphConstructor import GraphConstructor

        organisations = Organization.objects.filter(relations=relations)
        StateReturner.relations_all_paths_clear(relations)
        StateReturner.relations_objects_state_return(relations)
        if not relations.graph_structure:
            GraphConstructor.generate_graph_structure(relations)
        Navigator.normalize_bidirectional_paths(relations)
        # Перебираем все организации и пересчитываем пути
        for organization in organisations:
            Navigator.calculate_path_for_organization(organization)

    @staticmethod
    def normalize_bidirectional_paths(relations):
        from waste.models import Connection

        graph = relations.graph_structure
        if not graph or 'edges' not in graph:
            return

        edges = graph['edges']

        edge_map = {(edge['from'], edge['to']): edge for edge in edges}

        processed_pairs = set()

        for edge in edges:
            forward_key = (edge['from'], edge['to'])
            reverse_key = (edge['to'], edge['from'])

            if forward_key in processed_pairs or reverse_key in processed_pairs:
                continue

            if reverse_key in edge_map:
                reverse_edge = edge_map[reverse_key]
                reverse_edge['distance'] = edge['distance']

                # Обновляем связь в базе данных
                connection = Connection.objects.filter(id=reverse_edge['id']).first()
                if connection:
                    connection.distance = edge['distance']
                    connection.save()

            # Помечаем пару как обработанную
            processed_pairs.add(forward_key)
            processed_pairs.add(reverse_key)

        relations.graph_structure['edges'] = edges
        relations.save()

