# thermometer_app/thermometers/views.py
from rest_framework import viewsets, permissions
from django.shortcuts import render
from .models import Thermometer, Measurement
from .serializers import ThermometerSerializer, MeasurementSerializer

class ThermometerViewSet(viewsets.ModelViewSet):
    queryset = Thermometer.objects.all()
    serializer_class = ThermometerSerializer

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            permission_classes = [permissions.IsAdminUser]  # Только админы могут изменять термометры
        else:
            permission_classes = [permissions.AllowAny]  # Любой может просматривать
        return [permission() for permission in permission_classes]

class MeasurementViewSet(viewsets.ModelViewSet):
    serializer_class = MeasurementSerializer

    def get_queryset(self):
        queryset = Measurement.objects.all()
        thermometer_id = self.request.query_params.get('thermometer', None)
        if thermometer_id is not None:
            queryset = queryset.filter(thermometer_id=thermometer_id)
        return queryset

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            permission_classes = [permissions.IsAdminUser]  # Только админы могут изменять измерения
        else:
            permission_classes = [permissions.AllowAny]  # Любой может просматривать
        return [permission() for permission in permission_classes]

def index(request):
    thermometers = Thermometer.objects.all()
    return render(request, 'thermometers/index.html', {'thermometers': thermometers})