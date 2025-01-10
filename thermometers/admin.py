from django.contrib import admin
from django.contrib.auth.models import Group
from .models import Thermometer, Measurement

# Регистрируем группы в админке
admin.site.unregister(Group)
admin.site.register(Group)

# Регистрируем модели в админке
@admin.register(Thermometer)
class ThermometerAdmin(admin.ModelAdmin):
    list_display = ('name', 'location')
    search_fields = ('name', 'location')

@admin.register(Measurement)
class MeasurementAdmin(admin.ModelAdmin):
    list_display = ('thermometer', 'temperature', 'timestamp')
    list_filter = ('thermometer', 'timestamp')
    search_fields = ('thermometer__name',)