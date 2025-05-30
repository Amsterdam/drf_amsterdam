from rest_framework import routers

from .views import (PersonViewSet, SimpleViewSet, TemperatureRecordViewSet,
                    ThingViewSet, WeatherStationViewSet)


class ClimateAPI(routers.APIRootView):
    """
    Example API KNMI climate data.

    Note: this is used for testing drf_amsterdam project.
    """

    def get_api_root_view(self, **kwargs):
        view = super().get_api_root_view(**kwargs)
        cls = view.cls

        class Climate(cls):
            def get_view_name(self):
                return 'Example API KNMI climate data'

        Climate.__doc__ = self.__doc__
        return Climate.as_view()


class ApiRouter(routers.DefaultRouter):
    """The main router"""
    APIRootView = ClimateAPI


router = ApiRouter()
router.register('weatherstation', WeatherStationViewSet)
router.register('temperature_record', TemperatureRecordViewSet)
router.register('simple', SimpleViewSet)
router.register('thing', ThingViewSet)
router.register('person', PersonViewSet)
router.register('person.api', PersonViewSet, basename='person_api')

urlpatterns = router.urls
