from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'organizations', views.OrganizationView, basename='organizations')
router.register(r'relations', views.RelationsView, basename='relations')
router.register(r'waste_storages', views.WasteStorageView, basename='waste_storages')
router.register(r'connections', views.ConnectionView, basename='connections')

app_name = 'waste'

urlpatterns = [
    path('', include(router.urls)),
]
