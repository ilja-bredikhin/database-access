from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ThermometerViewSet, MeasurementViewSet, index

router = DefaultRouter()
router.register(r'thermometers', ThermometerViewSet)
router.register(r'measurements', MeasurementViewSet, basename='measurement')

urlpatterns = [
    path('', index, name='index'),
    path('api/', include(router.urls)),
]