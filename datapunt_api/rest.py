from collections import OrderedDict

from rest_framework import renderers, serializers
from rest_framework import viewsets
from rest_framework.reverse import reverse
from rest_framework_extensions.mixins import DetailSerializerMixin
from django_filters.rest_framework import DjangoFilterBackend

from .pagination import HALPagination

DEFAULT_RENDERERS = (renderers.JSONRenderer, renderers.BrowsableAPIRenderer)
FORMATS = [dict(format=r.format, type=r.media_type) for r in DEFAULT_RENDERERS]


def get_links(view_name, kwargs=None, request=None):
    result = OrderedDict([
        ('self', dict(
            href=reverse(view_name, kwargs=kwargs, request=request)
        ))
    ])

    return result


class DataSetSerializerMixin(object):
    def to_representation(self, obj):
        result = super(obj).to_representation(obj)
        result['dataset'] = self.dataset
        return result


class LinksField(serializers.HyperlinkedIdentityField):

    def to_representation(self, value):
        request = self.context.get('request')

        result = OrderedDict([
            ('self', dict(
                href=self.get_url(value, self.view_name, request, None))
             ),
        ])

        return result


class HALSerializer(serializers.HyperlinkedModelSerializer):
    url_field_name = '_links'
    serializer_url_field = LinksField


class _DisabledHTMLFilterBackend(DjangoFilterBackend):
    """
    See https://github.com/tomchristie/django-rest-framework/issues/3766
    This prevents DRF from generating the filter dropdowns which can
    be HUGE
    """

    def to_html(self, request, queryset, view):
        return ""


class DatapuntViewSet(DetailSerializerMixin, viewsets.ReadOnlyModelViewSet):
    """
    ViewSet subclass for use in Datapunt APIs.

    Note:
    - this uses HAL JSON style pagination.
    """
    renderer_classes = DEFAULT_RENDERERS
    pagination_class = HALPagination
    filter_backends = (_DisabledHTMLFilterBackend,)


class RelatedSummaryField(serializers.Field):
    def to_representation(self, value):
        count = value.count()
        model_name = value.model.__name__
        mapping = model_name.lower() + "-list"
        url = reverse(mapping, request=self.context['request'])

        parent_pk = value.instance.pk
        filter_name = list(value.core_filters.keys())[0]

        return dict(
            count=count,
            href="{}?{}={}".format(url, filter_name, parent_pk),
        )


# Note about DisplayField below; setting source to '*' causes the
# whole (model) instance to be passed to the DisplayField See:
# http://www.django-rest-framework.org/api-guide/fields/#source
# Display field then uses the __str__ function on the Django
# model to get a nice string representation that can be presented
# to the user.

class DisplayField(serializers.Field):
    """
    Add a `_display` field, based on Model string representation.
    """
    def __init__(self, *args, **kwargs):
        kwargs['source'] = '*'
        kwargs['read_only'] = True
        super().__init__(*args, **kwargs)

    def to_representation(self, value):
        return str(value)
