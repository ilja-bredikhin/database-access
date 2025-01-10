from django.db import models

class Thermometer(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.name} at {self.location}"

class Measurement(models.Model):
    thermometer = models.ForeignKey(Thermometer, on_delete=models.CASCADE)
    temperature = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.temperature}°C at {self.timestamp}"