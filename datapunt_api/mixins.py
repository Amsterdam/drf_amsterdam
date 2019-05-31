from rest_framework import mixins as drf_mixins
from rest_framework_extensions import mixins as drf_extensions_mixins

from datapunt_api.settings import api_settings


class DetailedRequestMixin(drf_extensions_mixins.DetailSerializerMixin):
    detailed_keyword = api_settings.DETAILED_KEYWORD

    def _is_detailed_request(self, request):
        value = request.GET.get(self.detailed_keyword, False)
        return value and value in [1, '1', True, 'True', 'true', 'Yes', 'yes']


class CreateModelMixin(drf_mixins.CreateModelMixin):
    pass


class ListModelMixin(DetailedRequestMixin, drf_mixins.ListModelMixin):
    def list(self, request, *args, **kwargs):
        if self._is_detailed_request(request):
            self.serializer_class = self.serializer_detail_class
        return super(DetailedRequestMixin, self).list(request=request, *args, **kwargs)


class RetrieveModelMixin(DetailedRequestMixin, drf_mixins.RetrieveModelMixin):
    pass


class UpdateModelMixin(drf_mixins.UpdateModelMixin):
    pass


class DestroyModelMixin(drf_mixins.DestroyModelMixin):
    pass
