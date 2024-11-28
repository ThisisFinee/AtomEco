import pytest
from rest_framework.test import APIClient
from waste.models import Connection, Organization, Relations, WasteStorage
from waste.workfiles.Generator import Generator
import random
import json


@pytest.mark.django_db
class TestViews:
    @pytest.fixture
    def client(self):
        return APIClient()

    @pytest.fixture
    def test_relations(self):
        return Generator.generate_random_graph("Test Relations")

    @pytest.fixture
    def test_relations_2(self):
        return Generator.generate_random_graph("Test Relations_2")

    @pytest.fixture
    def test_connection(self, test_relations):
        return random.choice(Connection.objects.filter(relations=test_relations))

    @pytest.fixture
    def test_organization(self, test_relations):
        return random.choice(Organization.objects.filter(relations=test_relations))

    @pytest.fixture
    def test_waste_storage(self, test_relations):
        return random.choice(WasteStorage.objects.filter(relations=test_relations))

    @pytest.fixture
    def test_connection_delete_obj(self, test_relations_delete_obj):
        return random.choice(Connection.objects.filter(relations=test_relations_delete_obj))

    @pytest.fixture
    def test_organization_delete_obj(self, test_relations_delete_obj):
        return random.choice(Organization.objects.filter(relations=test_relations_delete_obj))

    @pytest.fixture
    def test_waste_storage_delete_obj(self, test_relations_delete_obj):
        return random.choice(WasteStorage.objects.filter(relations=test_relations_delete_obj))

    @pytest.fixture
    def test_relations_delete_obj(self):
        return Generator.generate_random_graph("Test Relations_delete")

    def test_connection_detail(self, client, test_connection):
        response = client.get(f"/waste/connections/{test_connection.id}/")
        assert response.status_code == 200
        assert response.data["id"] == test_connection.id

    def test_organization_detail(self, client, test_organization):
        response = client.get(f"/waste/organizations/{test_organization.id}/")
        assert response.status_code == 200
        assert response.data["id"] == test_organization.id

    def test_relations_detail(self, client, test_relations):
        response = client.get(f"/waste/relations/{test_relations.id}/")
        assert response.status_code == 200
        assert response.data["id"] == test_relations.id

    def test_waste_storage_detail(self, client, test_waste_storage):
        response = client.get(f"/waste/waste_storages/{test_waste_storage.id}/")
        assert response.status_code == 200
        assert response.data["id"] == test_waste_storage.id

    def test_connection_update(self, client, test_connection):
        data = {"distance": 900}
        response = client.patch(f"/waste/connections/{test_connection.id}/",
                                data=json.dumps(data), content_type="application/json")
        assert response.status_code == 200
        test_connection.refresh_from_db()
        assert test_connection.distance == 900

    def test_organization_update(self, client, test_organization):
        data = {"name": "Updated Organization", "generate_glass": 200, "generate_plastic": 200,
                "generate_bio_wastes": 200}
        response = client.patch(f"/waste/organizations/{test_organization.id}/",
                                data=json.dumps(data), content_type="application/json")
        assert response.status_code == 200
        test_organization.refresh_from_db()
        assert test_organization.name == "Updated Organization" \
               and test_organization.generate_glass == 200 and test_organization.generate_plastic == 200 \
               and test_organization.generate_bio_wastes == 200

    def test_relations_update(self, client, test_relations):
        data = {"relations_name": "Updated Relations"}
        response = client.patch(f"/waste/relations/{test_relations.id}/",
                                data=json.dumps(data), content_type="application/json")
        assert response.status_code == 200
        test_relations.refresh_from_db()
        assert test_relations.relations_name == "Updated Relations"

    def test_waste_storage_update(self, client, test_waste_storage):
        data = {"name": "Updated Waste Storage", "max_glass": 200, "max_plastic": 200, "max_bio_wastes": 200}
        response = client.patch(f"/waste/waste_storages/{test_waste_storage.id}/",
                                data=json.dumps(data), content_type="application/json")
        assert response.status_code == 200
        test_waste_storage.refresh_from_db()
        assert test_waste_storage.name == "Updated Waste Storage" \
               and test_waste_storage.max_glass == 200 and test_waste_storage.max_plastic == 200 \
               and test_waste_storage.max_bio_wastes == 200

    def test_connection_delete(self, client, test_connection_delete_obj):
        response = client.delete(f"/waste/connections/{test_connection_delete_obj.id}/")
        assert response.status_code == 204
        assert not Connection.objects.filter(id=test_connection_delete_obj.id).exists()

    def test_organization_delete(self, client, test_organization_delete_obj):
        response = client.delete(f"/waste/organizations/{test_organization_delete_obj.id}/")
        assert response.status_code == 204
        assert not Organization.objects.filter(id=test_organization_delete_obj.id).exists()
        assert not Connection.objects.filter(first_point=test_organization_delete_obj).exists() \
               and not Connection.objects.filter(second_point=test_organization_delete_obj).exists()

    def test_waste_storage_delete(self, client, test_waste_storage_delete_obj):
        response = client.delete(f"/waste/waste_storages/{test_waste_storage_delete_obj.id}/")
        assert response.status_code == 204
        assert not WasteStorage.objects.filter(id=test_waste_storage_delete_obj.id).exists()

    def test_relations_delete(self, client, test_relations_delete_obj):
        response = client.delete(f"/waste/relations/{test_relations_delete_obj.id}/")
        assert response.status_code == 204
        assert not Relations.objects.filter(id=test_relations_delete_obj.id).exists()
        assert not Connection.objects.filter(relations=test_relations_delete_obj).exists() \
               and not WasteStorage.objects.filter(relations=test_relations_delete_obj).exists() \
               and not Organization.objects.filter(relations=test_relations_delete_obj).exists()

    def test_connection_list(self, client):
        response = client.get("/waste/connections/")
        assert response.status_code == 200

    def test_connection_create(self, client, test_relations_2):
        len_of_connections = Connection.objects.filter(relations=test_relations_2).count()
        first_point = Organization.objects.filter(relations=test_relations_2).first()
        second_point = WasteStorage.objects.filter(relations=test_relations_2).first()

        response = client.post(
            "/waste/connections/",
            data={
                "relations": test_relations_2.id,
                "first_point": first_point.id,
                "second_point": second_point.id,
                "distance": 615,
            },
        )

        assert response.status_code == 201
        assert Connection.objects.filter(relations=test_relations_2).count() > len_of_connections

    def test_organization_list(self, client):
        response = client.get("/waste/organizations/")
        assert response.status_code == 200

    def test_organization_create(self, client, test_relations_2):
        len_of_organizations = Organization.objects.filter(relations=test_relations_2).count()
        response = client.post(
            "/waste/organizations/",
            data={
                "relations": test_relations_2.id,
                "name": "Test Org Create",
                "generate_plastic": 50,
                "generate_glass": 30,
                "generate_bio_wastes": 20,
            },
        )
        new_len_of_organization = Organization.objects.filter(relations=test_relations_2).count()
        assert response.status_code == 201
        assert new_len_of_organization > len_of_organizations

    def test_relations_list(self, client):
        response = client.get("/waste/relations/")
        assert response.status_code == 200

    def test_relations_recalculate_paths(self, client):
        relations = Generator.generate_random_graph("Test Relations recalculate")
        response = client.patch(f"/waste/relations/{relations.id}/recalculate_paths/")
        assert response.status_code == 201
        assert "Paths recalculated successfully" in response.data["message"]

    def test_relations_generate_graph_structure(self, client):
        relations = Generator.generate_random_graph("Test Relations generate")
        response = client.patch(f"/waste/relations/{relations.id}/generate_graph_structure/")
        assert response.status_code == 201
        assert "Graph structure generated successfully" in response.data["message"]

    # WasteStorage
    def test_waste_storage_list(self, client):
        response = client.get("/waste/waste_storages/")
        assert response.status_code == 200

    def test_waste_storage_create(self, client, test_relations_2):
        len_of_storages = WasteStorage.objects.filter(relations=test_relations_2).count()
        response = client.post(
            "/waste/waste_storages/",
            data={
                "relations": test_relations_2.id,
                "name": "Test Storage",
                "generate_plastic": 50,
                "generate_glass": 30,
                "generate_bio_wastes": 20,
            },
        )
        new_len_of_storages = WasteStorage.objects.filter(relations=test_relations_2).count()
        assert response.status_code == 201
        assert len_of_storages < new_len_of_storages

    #  Generate_graph_tests
    def test_generate_base_graph(self, client):
        response = client.post("/waste/relations/generate_graph/?type=base")
        assert response.status_code == 201
        assert "Graph of type 'base' generated successfully." in response.data['message']

    def test_generate_spec_graph_valid(self, client):
        response = client.post("/waste/relations/generate_graph/?type=spec")
        assert response.status_code == 201
        assert "Graph of type 'spec' generated successfully." in response.data['message']
        assert response.data['relations'] is not None

    def test_generate_intersection_graph_valid(self, client):
        response = client.post("/waste/relations/generate_graph/?type=intersection")
        assert response.status_code == 201
        assert "Graph of type 'intersection' generated successfully." in response.data['message']
        assert response.data['relations'] is not None

    def test_generate_error_graph_valid(self, client):
        response = client.post("/waste/relations/generate_graph/?type=error")
        assert response.status_code == 201
        assert "Graph of type 'error' generated successfully." in response.data['message']
        assert response.data['relations'] is not None

    def test_generate_graph_invalid_type(self, client):
        response = client.post("/waste/relations/generate_graph/?type=invalid")
        assert response.status_code == 400
        assert "Unknown graph type: invalid" in response.data['error']

    def test_generate_base_graph_missing_type(self, client):
        response = client.post("/waste/relations/generate_graph/")
        assert response.status_code == 400
        assert "Parameter 'type' is required." in response.data['error']

    def test_generate_random_full_graphs(self, client):
        response = client.post('/waste/relations/generate_random_graphs/?type=full&number=2')
        assert response.status_code == 201
        assert "Graphs of type 'full', graphs number: 2, generated successfully." in response.data['message']
        assert len(response.data["all_generate_relations"]) == 2

    def test_generate_random_partial_graph(self, client):
        response = client.post('/waste/relations/generate_random_graphs/?type=partial&number=2')
        assert response.status_code == 201
        assert "Graphs of type 'partial', graphs number: 2, generated successfully." in response.data['message']
        assert len(response.data["all_generate_relations"]) == 2
