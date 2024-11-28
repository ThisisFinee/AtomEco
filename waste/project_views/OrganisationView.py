from rest_framework import viewsets
from waste.models import Organization
from waste.serializers import OrganizationSerializer


class OrganizationView(viewsets.ModelViewSet):
    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer
