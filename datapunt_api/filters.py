from django_filters.rest_framework import DjangoFilterBackend


class DisabledHTMLFilterBackend(DjangoFilterBackend):
    """
    See https://github.com/tomchristie/django-rest-framework/issues/3766.

    This prevents DRF from generating the filter dropdowns (which can be HUGE
    in our case)
    """
    def to_html(self, request, queryset, view):
        return ""
