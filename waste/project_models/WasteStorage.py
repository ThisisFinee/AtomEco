from django.db import models
from waste.project_models.BasePoint import BasePoint


class WasteStorage(BasePoint):
    max_plastic = models.IntegerField(null=True, blank=True, default=0)
    max_glass = models.IntegerField(null=True, blank=True, default=0)
    max_bio_wastes = models.IntegerField(null=True, blank=True, default=0)
    plastic = models.IntegerField(null=True, blank=True, default=0)
    glass = models.IntegerField(null=True, blank=True, default=0)
    bio_wastes = models.IntegerField(null=True, blank=True, default=0)
