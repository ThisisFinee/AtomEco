from rest_framework import viewsets
from waste.models import WasteStorage
from waste.serializers import WasteStorageSerializer


class WasteStorageView(viewsets.ModelViewSet):
    queryset = WasteStorage.objects.all()
    serializer_class = WasteStorageSerializer
