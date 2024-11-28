from waste.models import Organization, WasteStorage, Connection, Relations
from waste.workfiles.GraphConstructor import GraphConstructor
from waste.workfiles.Navigator import Navigator
import random


def ensure_connected_graph(nodes, relations):
    visited = set()

    def dfs(node_id):
        visited.add(node_id)
        for connection in Connection.objects.filter(relations=relations):
            if connection.first_point.id == node_id and connection.second_point.id not in visited:
                dfs(connection.second_point.id)
            elif connection.second_point.id == node_id and connection.first_point.id not in visited:
                dfs(connection.first_point.id)

    dfs(nodes[0].id)
    if len(visited) != len(nodes):
        isolated_nodes = [n for n in nodes if n.id not in visited]
        for isolated_node in isolated_nodes:
            nearest_node = random.choice([n for n in nodes if n.id not in isolated_nodes])
            distance = random.randint(10, 500)
            Connection.objects.create(first_point=isolated_node, second_point=nearest_node, distance=distance,
                                      relations=relations)


class Generator:

    @staticmethod
    def generate_test_graph():
        relations = Relations.objects.create(relations_name="Test Graph")

        org1 = Organization.objects.create(
            name="ОО 1",
            relations=relations,
            generate_plastic=10,
            generate_glass=50,
            generate_bio_wastes=50,
        )
        org2 = Organization.objects.create(
            name="ОО 2",
            relations=relations,
            generate_plastic=60,
            generate_glass=20,
            generate_bio_wastes=50,
        )

        storage1 = WasteStorage.objects.create(name="МНО 1", relations=relations, max_plastic=100,
                                               max_glass=300)
        storage2 = WasteStorage.objects.create(name="МНО 2", relations=relations, max_plastic=50,
                                               max_bio_wastes=150)
        storage3 = WasteStorage.objects.create(name="МНО 3", relations=relations, max_plastic=10,
                                               max_bio_wastes=250)
        storage6 = WasteStorage.objects.create(name="МНО 6", relations=relations, max_glass=100,
                                               max_bio_wastes=150)
        storage5 = WasteStorage.objects.create(name="МНО 5", relations=relations, max_glass=220,
                                               max_bio_wastes=25)
        storage7 = WasteStorage.objects.create(name="МНО 7", relations=relations, max_plastic=100,
                                               max_bio_wastes=250)
        storage8 = WasteStorage.objects.create(name="МНО 8", relations=relations, max_plastic=25, max_glass=35,
                                               max_bio_wastes=52)
        storage9 = WasteStorage.objects.create(name="МНО 9", relations=relations, max_plastic=250,
                                               max_bio_wastes=20)

        connections = [
            (org1, storage1, 100),
            (org1, storage2, 50),
            (org1, storage3, 600),
            (org2, storage3, 50),
            (storage1, storage8, 500),
            (storage8, storage9, 10),
            (storage9, storage8, 10),
            (storage2, storage5, 50),
            (storage5, storage2, 50),
            (storage3, storage7, 50),
            (storage7, storage3, 50),
            (storage3, storage6, 600),
        ]

        for from_node, to_node, distance in connections:
            Connection.objects.create(first_point=from_node, second_point=to_node, distance=distance,
                                      relations=relations)

        # Генерация графа
        GraphConstructor.generate_graph_structure(relations)
        Navigator.recalculate_all_paths(relations)
        return relations

    @staticmethod
    def generate_specific_graph():
        relations = Relations.objects.create(relations_name="Specific Graph")

        org1 = Organization.objects.create(
            name="Spec_ОО 1",
            relations=relations,
            generate_plastic=525,
            generate_glass=555,
            generate_bio_wastes=347,
        )
        org2 = Organization.objects.create(
            name="Spec_ОО 2",
            relations=relations,
            generate_plastic=110,
            generate_glass=100,
            generate_bio_wastes=650,
        )

        storage1 = WasteStorage.objects.create(name="Spec_МНО 1", relations=relations, max_plastic=100,
                                               max_glass=300)
        storage2 = WasteStorage.objects.create(name="Spec_МНО 2", relations=relations, max_plastic=50,
                                               max_bio_wastes=150)
        storage3 = WasteStorage.objects.create(name="Spec_МНО 3", relations=relations, max_plastic=10,
                                               max_bio_wastes=250)
        storage6 = WasteStorage.objects.create(name="Spec_МНО 6", relations=relations, max_glass=100,
                                               max_bio_wastes=150)
        storage5 = WasteStorage.objects.create(name="Spec_МНО 5", relations=relations, max_glass=220,
                                               max_bio_wastes=25)
        storage7 = WasteStorage.objects.create(name="Spec_МНО 7", relations=relations, max_plastic=100,
                                               max_bio_wastes=250)
        storage8 = WasteStorage.objects.create(name="Spec_МНО 8", relations=relations, max_plastic=25, max_glass=35,
                                               max_bio_wastes=52)
        storage9 = WasteStorage.objects.create(name="Spec_МНО 9", relations=relations, max_plastic=250,
                                               max_bio_wastes=20)
        storage4 = WasteStorage.objects.create(name="Spec_МНО 4", relations=relations, max_plastic=100,
                                               max_bio_wastes=100)

        connections = [
            (org1, storage1, 100),
            (org1, storage2, 50),
            (org2, storage3, 50),
            (storage1, storage8, 500),
            (storage1, storage4, 600),
            (storage8, storage9, 10),
            (storage9, storage8, 10),
            (storage2, storage5, 50),
            (storage5, storage2, 50),
            (storage3, storage7, 50),
            (storage7, storage3, 50),
            (storage3, storage6, 600),
        ]

        for from_node, to_node, distance in connections:
            Connection.objects.create(first_point=from_node, second_point=to_node, distance=distance,
                                      relations=relations)

        # Генерация графа
        GraphConstructor.generate_graph_structure(relations)
        Navigator.recalculate_all_paths(relations)
        return relations

    @staticmethod
    def generate_graph_with_intersections():
        relations = Relations.objects.create(relations_name="Specific Graph")

        org1 = Organization.objects.create(
            name="Spec_ОО 1",
            relations=relations,
            generate_plastic=500,
            generate_glass=300,
            generate_bio_wastes=500,
        )
        org2 = Organization.objects.create(
            name="Spec_ОО 2",
            relations=relations,
            generate_plastic=205,
            generate_glass=100,
            generate_bio_wastes=300,
        )

        storage1 = WasteStorage.objects.create(name="Spec_МНО 1", relations=relations, max_plastic=100,
                                               max_glass=100)
        storage2 = WasteStorage.objects.create(name="Spec_МНО 2", relations=relations, max_plastic=105,
                                               max_bio_wastes=100)
        storage3 = WasteStorage.objects.create(name="Spec_МНО 3", relations=relations, max_plastic=100,
                                               max_bio_wastes=100)
        storage6 = WasteStorage.objects.create(name="Spec_МНО 6", relations=relations, max_glass=100,
                                               max_bio_wastes=100)
        storage5 = WasteStorage.objects.create(name="Spec_МНО 5", relations=relations, max_glass=100,
                                               max_bio_wastes=100)
        storage7 = WasteStorage.objects.create(name="Spec_МНО 7", relations=relations, max_plastic=100,
                                               max_bio_wastes=100)
        storage8 = WasteStorage.objects.create(name="Spec_МНО 8", relations=relations, max_plastic=100, max_glass=100,
                                               max_bio_wastes=100)
        storage9 = WasteStorage.objects.create(name="Spec_МНО 9", relations=relations, max_plastic=100,
                                               max_bio_wastes=100)
        storage4 = WasteStorage.objects.create(name="Spec_МНО 4", relations=relations, max_plastic=100,
                                               max_bio_wastes=100)

        connections = [
            (org1, storage1, 100),
            (org1, storage2, 50),
            (org2, storage3, 50),
            (org2, storage1, 100),
            (storage1, storage8, 500),
            (storage1, storage4, 600),
            (storage8, storage9, 10),
            (storage9, storage8, 10),
            (storage2, storage5, 50),
            (storage5, storage2, 50),
            (storage3, storage7, 50),
            (storage7, storage3, 50),
            (storage3, storage6, 600),
        ]

        for from_node, to_node, distance in connections:
            Connection.objects.create(first_point=from_node, second_point=to_node, distance=distance,
                                      relations=relations)

        # Генерация графа
        GraphConstructor.generate_graph_structure(relations)
        Navigator.recalculate_all_paths(relations)
        return relations

    @staticmethod
    def generate_error_graph():
        relations = Relations.objects.create(relations_name="Specific Graph")

        org1 = Organization.objects.create(
            name="Spec_ОО 1",
            relations=relations,
            generate_plastic=300,
            generate_glass=300,
            generate_bio_wastes=300,
        )
        org2 = Organization.objects.create(
            name="Spec_ОО 2",
            relations=relations,
            generate_plastic=300,
            generate_glass=300,
            generate_bio_wastes=300,
        )

        storage1 = WasteStorage.objects.create(name="Spec_МНО 1", relations=relations, max_plastic=100,
                                               max_glass=100)
        storage2 = WasteStorage.objects.create(name="Spec_МНО 2", relations=relations, max_plastic=105,
                                               max_bio_wastes=100)
        storage3 = WasteStorage.objects.create(name="Spec_МНО 3", relations=relations, max_plastic=100,
                                               max_bio_wastes=100)
        storage6 = WasteStorage.objects.create(name="Spec_МНО 6", relations=relations, max_glass=100,
                                               max_bio_wastes=100)

        connections = [
            (org1, storage1, 100),
            (org1, storage2, 50),
            (org2, storage3, 50),
            (org2, storage1, 100),
            (storage3, storage6, 600),
        ]

        for from_node, to_node, distance in connections:
            Connection.objects.create(first_point=from_node, second_point=to_node, distance=distance,
                                      relations=relations)

        # Генерация графа
        GraphConstructor.generate_graph_structure(relations)
        Navigator.recalculate_all_paths(relations)
        return relations

    @staticmethod
    def generate_random_graph(name, full_discharge=True):
        relations = Relations.objects.create(relations_name=name)
        relations.relations_name = f"{name} {relations.id}"

        organizations = []
        for i in range(random.randint(3, 5)):
            organizations.append(
                Organization.objects.create(
                    name="",
                    relations=relations,
                    generate_plastic=random.randint(10, 100),
                    generate_glass=random.randint(10, 100),
                    generate_bio_wastes=random.randint(10, 100),
                )
            )
            organizations[i].name = f"Organization_{organizations[i].id}"
            organizations[i].save()

        storages = []
        min_storages, max_storages = 3, 6
        if full_discharge:
            min_storages = len(organizations)*2
            max_storages = min_storages + 3
        for i in range(random.randint(min_storages, max_storages)):
            storages.append(
                WasteStorage.objects.create(
                    name="",
                    relations=relations,
                    max_plastic=random.randint(50, 150) if full_discharge else random.randint(0, 50),
                    max_glass=random.randint(50, 150) if full_discharge else random.randint(0, 50),
                    max_bio_wastes=random.randint(50, 150) if full_discharge else random.randint(0, 50),
                )
            )
            storages[i].name = f"Storage_{storages[i].id}"
            storages[i].save()

        for org in organizations:
            storages_to_connect = random.sample(storages, k=random.randint(1, len(storages)))
            for storage in storages_to_connect:
                distance = random.randint(10, 500)
                Connection.objects.create(first_point=org, second_point=storage, distance=distance, relations=relations)

        connected_pairs = set()
        for storage1 in storages:
            for _ in range(random.randint(1, len(storages) - 1)):
                storage2 = random.choice(
                    [s for s in storages if s != storage1 and (storage1.id, s.id) not in connected_pairs])
                connected_pairs.add((storage1.id, storage2.id))
                distance = random.randint(10, 600)
                Connection.objects.create(first_point=storage1, second_point=storage2, distance=distance,
                                          relations=relations)

        ensure_connected_graph(organizations + storages, relations)

        GraphConstructor.generate_graph_structure(relations)
        Navigator.recalculate_all_paths(relations)
        return relations

    @staticmethod
    def generate_fully_graphs(n=5):
        graphs = []
        for i in range(n):
            graphs.append(Generator.generate_random_graph(name=f"Full graph", full_discharge=True))
        return graphs

    @staticmethod
    def generate_partially_graphs(n=5):
        graphs = []
        for i in range(n):
            graphs.append(Generator.generate_random_graph(name=f"Partially graph", full_discharge=False))
        return graphs
