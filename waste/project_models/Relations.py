from django.db import models


class Relations(models.Model):
    graph_structure = models.JSONField(null=True, blank=True)
    ways_structure = models.JSONField(null=True, blank=True)
    relations_name = models.TextField(null=True, blank=True)

    def delete(self, *args, **kwargs):
        from waste.models import WasteStorage, Organization, Connection

        Connection.objects.filter(relations=self).delete()
        Organization.objects.filter(relations=self).delete()
        WasteStorage.objects.filter(relations=self).delete()

        super().delete(*args, **kwargs)


""" graph_structure
{
    "nodes": [
        {"id": 1, "type": "Organization", "name": "Org A"},
        {"id": 2, "type": "WasteStorage", "name": "Storage 1"},
        {"id": 3, "type": "WasteStorage", "name": "Storage 2"}
    ],
    "edges": [
        {"from": 1, "to": 2, "distance": 50, "id": 5},
        {"from": 2, "to": 3, "distance": 30, "id": 6}
    ]
}
"""


""" ways_structure
{
  "1": {
    "error": false,
    "paths": [
      {
        "path": [
          [
            1,
            2
          ],
          5
        ],
        "distance": 50,
        "waste_distribution": {
          "glass": 0,
          "plastic": 10,
          "bio_wastes": 50
        }
      },
      {
        "path": [
          [
            2,
            3
          ],
          6
        ],
        "distance": 30,
        "waste_distribution": {
          "glass": 50,
          "plastic": 0,
          "bio_wastes": 0
        }
      }
    ],
    "result_path": [
      [
        1,
        2
      ],
      [
        2,
        3
      ]
    ],
    "result_distance": 80
  }
}
"""
