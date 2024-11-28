from django.db import models
from waste.project_models.Relations import Relations
from waste.project_models.BasePoint import BasePoint


class Connection(models.Model):
    relations = models.ForeignKey(Relations, on_delete=models.CASCADE)
    first_point = models.ForeignKey(BasePoint, on_delete=models.CASCADE, related_name='first_point')
    second_point = models.ForeignKey(BasePoint, on_delete=models.CASCADE, related_name='second_point')
    distance = models.IntegerField(blank=True)
