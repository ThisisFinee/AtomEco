from rest_framework import viewsets
from waste.models import Connection
from waste.serializers import ConnectionSerializer


class ConnectionView(viewsets.ModelViewSet):
    queryset = Connection.objects.all()
    serializer_class = ConnectionSerializer
