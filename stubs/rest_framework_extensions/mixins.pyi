from typing import Generic, TypeVar

from django.db.models import Model, QuerySet
from rest_framework.serializers import BaseSerializer

_MT_co = TypeVar("_MT_co", bound=Model, covariant=True)

class DetailSerializerMixin(Generic[_MT_co]):
    serializer_detail_class: type[BaseSerializer[_MT_co]]
    queryset_detail: QuerySet[_MT_co]

    def get_serializer_class(self) -> type[BaseSerializer[_MT_co]]: ...
    def get_queryset(self) -> QuerySet[_MT_co]: ...
    def _is_request_to_detail_endpoint(self) -> bool: ...
