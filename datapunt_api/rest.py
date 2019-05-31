""" Will be deprecated soon """
from .viewsets import DatapuntReadOnlyViewSet, DatapuntWritableViewSet
from .serializers import *  # noqa


class DatapuntViewSet(DatapuntReadOnlyViewSet):
    pass


class DatapuntViewSetWritable(DatapuntWritableViewSet):
    pass
