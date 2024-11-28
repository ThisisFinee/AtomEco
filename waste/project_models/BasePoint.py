from django.db import models
from polymorphic.models import PolymorphicModel
from waste.project_models.Relations import Relations


class BasePoint(PolymorphicModel):
    relations = models.ForeignKey(Relations, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name
