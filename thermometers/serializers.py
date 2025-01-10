from rest_framework import serializers
from .models import Thermometer, Measurement

class ThermometerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Thermometer
        fields = '__all__'

class MeasurementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Measurement
        fields = '__all__'