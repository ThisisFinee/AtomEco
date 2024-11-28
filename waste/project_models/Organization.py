from django.db import models
from waste.project_models.BasePoint import BasePoint


class Organization(BasePoint):
    generate_plastic = models.IntegerField(null=True, blank=True)
    generate_glass = models.IntegerField(null=True, blank=True)
    generate_bio_wastes = models.IntegerField(null=True, blank=True)
    plastic = models.IntegerField(null=True, blank=True)
    glass = models.IntegerField(null=True, blank=True)
    bio_wastes = models.IntegerField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if self.plastic is None:
            self.plastic = self.generate_plastic
        if self.glass is None:
            self.glass = self.generate_glass
        if self.bio_wastes is None:
            self.bio_wastes = self.generate_bio_wastes
        super().save(*args, **kwargs)
