"""
Serialization classes for Datapunt style Django REST Framework APIs.
"""
from collections import OrderedDict
from typing import Any, Mapping, TypeVar, TYPE_CHECKING, Generic, TypedDict

from django.contrib.gis.geos import Point, Polygon, MultiPolygon
from django.db.models import Model
from django.http import HttpRequest
from rest_framework import serializers
from rest_framework.request import Request
from rest_framework.reverse import reverse
import json

_IN = TypeVar("_IN")
_MT = TypeVar("_MT", bound=Model)


def get_links(
        view_name: str,
        kwargs: Mapping[str, Any] | None = None,
        request: HttpRequest | None = None
) -> OrderedDict[str, dict[str, str]]:
    result = OrderedDict([
        ('self', dict(
            href=reverse(view_name, kwargs=kwargs, request=request)
        ))
    ])

    return result


class DataSetSerializerMixin(serializers.BaseSerializer[_IN]):
    """Add dataset field to indicate 'source' of this data."""
    dataset: str

    def to_representation(self, obj: _IN) -> dict[str, Any]:
        result = super().to_representation(obj)
        result['dataset'] = self.dataset
        return result


if TYPE_CHECKING:
    class BaseLinksField(serializers.RelatedField[_MT, str, dict[str, dict[str, str | None]]]): pass
else:
    class BaseLinksField(Generic[_MT], serializers.RelatedField): pass


class LinksField(BaseLinksField[_MT]):
    lookup_field: str = 'pk'
    lookup_url_kwarg: str
    view_name: str | None = None

    def __init__(self, view_name: str | None = None, **kwargs):
        if view_name is not None:
            self.view_name = view_name
        assert self.view_name is not None, 'The `view_name` argument is required.'
        self.lookup_field = kwargs.pop('lookup_field', self.lookup_field)
        self.lookup_url_kwarg = kwargs.pop('lookup_url_kwarg', self.lookup_field)

        kwargs['read_only'] = True
        kwargs['source'] = '*'

        super().__init__(**kwargs)

    def to_representation(self, value: _MT) -> dict[str, dict[str, str | None]]:
        request = self.context.get('request')
        assert isinstance(request, Request)
        assert self.view_name is not None

        if hasattr(value, 'pk') and value.pk in (None, ''):
            href = None
        else:
            lookup_value = getattr(value, self.lookup_field)
            kwargs = {self.lookup_url_kwarg: lookup_value}
            href = reverse(self.view_name, kwargs=kwargs, request=request, format=None)

        return OrderedDict([('self', {
            'href': href
        })])


class HALSerializer(serializers.HyperlinkedModelSerializer):
    url_field_name: str = '_links'
    serializer_url_field: type[serializers.RelatedField] = LinksField


class SelfLinkSerializerMixin(serializers.BaseSerializer[_IN]):
    def get__links(self, obj: Model) -> dict[str, dict[str, str]]:
        """
        Serialization of _links field for detail view (assumes ModelViewSet).

        Note:
            Used to provide HAL-JSON style self links.
        """
        view = self.context['view']
        model = view.queryset.model
        pk_value = getattr(obj, model._meta.pk.name)

        return {
            'self': {
                'href': view.reverse_action('detail', args=[pk_value])
            }
        }


class RelatedSummaryField(serializers.Field):
    def to_representation(self, value) -> dict[str, str]:
        count = value.count()
        model_name = value.model.__name__
        mapping = model_name.lower() + "-list"
        url = reverse(mapping, request=self.context['request'])

        parent_pk = value.instance.pk
        filter_name = list(value.core_filters.keys())[0]

        return {
            'count': count,
            'href': f'{url}?{filter_name}={parent_pk}',
        }


# Note about DisplayField below; setting source to '*' causes the
# whole (model) instance to be passed to the DisplayField See:
# http://www.django-rest-framework.org/api-guide/fields/#source
# Display field then uses the __str__ function on the Django
# model to get a nice string representation that can be presented
# to the user.

if TYPE_CHECKING:
    class BaseDisplayField(serializers.Field[_MT, str, str, Any]): pass
else:
    class BaseDisplayField(Generic[_MT], serializers.Field): pass

class DisplayField(BaseDisplayField[_MT]):
    """
    Add a `_display` field, based on Model string representation.
    """
    def __init__(self, *args, **kwargs) -> None:
        kwargs['source'] = '*'
        kwargs['read_only'] = True
        super().__init__(*args, **kwargs)

    def to_representation(self, value: _MT) -> str:
        return str(value)


class GeoJson(TypedDict):
    type: str
    coordinates: list[float] | list[list[list[float]]] | list[list[list[list[float]]]]


class MultipleGeometryField(serializers.Field):
    read_only: bool = True

    def get_attribute(self, obj):
        return obj.geometrie

    def to_representation(self, value: Point | Polygon | MultiPolygon | None) -> str | GeoJson:
        res = ''
        if value:
            res = json.loads(value.geojson)

        return res
