from rest_framework import viewsets

from datasets.models import WeatherStation
from datasets.models import TemperatureRecord

from .serializers import WeatherStationSerializer
from .serializers import TemperatureRecordSerializer


class WeatherStationViewSet(viewsets.ModelViewSet):
    serializer_class = WeatherStationSerializer
    queryset = WeatherStation.objects.all()


class TemperatureRecordViewSet(viewsets.ModelViewSet):
    serializer_class = TemperatureRecordSerializer
    queryset = TemperatureRecord.objects.all().order_by('date')
