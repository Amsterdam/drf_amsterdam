from rest_framework import viewsets
from datapunt_api.rest import DatapuntViewSet

from datasets.models import WeatherStation
from datasets.models import TemperatureRecord

from .serializers import WeatherStationSerializer
from .serializers import TemperatureRecordSerializer


class WeatherStationViewSet(DatapuntViewSet):
    serializer_class = WeatherStationSerializer
    queryset = WeatherStation.objects.all()


class TemperatureRecordViewSet(DatapuntViewSet):
    serializer_class = TemperatureRecordSerializer
    queryset = TemperatureRecord.objects.all().order_by('date')
