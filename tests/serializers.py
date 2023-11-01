from rest_framework.serializers import ModelSerializer

from datapunt_api.rest import HALSerializer
from rest_framework import serializers

from datapunt_api.serializers import DataSetSerializerMixin, DisplayField, SelfLinkSerializerMixin
from tests import models

class WeatherStationSerializer(HALSerializer):
    class Meta:
        model = models.WeatherStation
        fields = '__all__'


class DatasetSerializer(DataSetSerializerMixin, HALSerializer):
    dataset = 'test_dataset'

    class Meta:
        model = models.SimpleModel
        fields = '__all__'


class SelfLinksSerializer(SelfLinkSerializerMixin, ModelSerializer):
    _links = serializers.SerializerMethodField()

    class Meta:
        model = models.SimpleModel
        fields = '__all__'


class WeatherDetailStationSerializer(HALSerializer):

    detailed = serializers.SerializerMethodField()

    class Meta:
        model = models.WeatherStation
        fields = [
            '_links',
            'number',
            'detailed'
        ]

    def get_detailed(self, obj):
        return 'I am detailed'


class TemperatureRecordSerializer(HALSerializer):
    class Meta:
        model = models.TemperatureRecord
        fields = '__all__'


class DisplayFieldSerializer(ModelSerializer):
    _display = DisplayField()

    class Meta:  # noqa
        model = models.WeatherStation
        fields = '__all__'
