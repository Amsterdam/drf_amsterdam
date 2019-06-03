from rest_framework.renderers import BrowsableAPIRenderer, JSONRenderer
from rest_framework.settings import api_settings
from rest_framework.viewsets import GenericViewSet
from rest_framework_xml.renderers import XMLRenderer

from . import mixins
from .filters import DisabledHTMLFilterBackend
from .pagination import HALPagination
from .renderers import PaginatedCSVRenderer


if api_settings.DEFAULT_RENDERER_CLASSES:
    DEFAULT_RENDERER_CLASSES = api_settings.DEFAULT_RENDERER_CLASSES
else:
    DEFAULT_RENDERER_CLASSES = [
        JSONRenderer,
        PaginatedCSVRenderer,
        BrowsableAPIRenderer,
        XMLRenderer,
    ]


class GenericDatapuntViewSet(GenericViewSet):
    renderer_classes = DEFAULT_RENDERER_CLASSES
    pagination_class = HALPagination
    filter_backends = (DisabledHTMLFilterBackend,)


class DatapuntReadOnlyViewSet(mixins.RetrieveModelMixin,
                              mixins.ListModelMixin,
                              GenericDatapuntViewSet):
    pass


class DatapuntWritableViewSet(mixins.CreateModelMixin,
                              mixins.RetrieveModelMixin,
                              mixins.UpdateModelMixin,
                              mixins.DestroyModelMixin,
                              mixins.ListModelMixin,
                              GenericDatapuntViewSet):
    pass
