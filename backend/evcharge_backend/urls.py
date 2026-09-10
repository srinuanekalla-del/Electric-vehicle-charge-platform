from django.contrib import admin
from django.shortcuts import redirect
from django.urls import include, path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

schema_view = get_schema_view(
    openapi.Info(
        title="EV Charging Platform API",
        default_version="v1",
        description="Stations, Chargers, Bookings, Payments, and Charging History.",
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)


def home(request):
    """
    Redirects the bare root URL ('/') to the Swagger docs page, so visitors
    land on something useful instead of Django's default 404.
    """
    return redirect('schema-swagger-ui')


urlpatterns = [
    path('', home),

    path('admin/', admin.site.urls),
    path('api/accounts/', include('accounts.urls')),
    path('api/', include('stations.urls')),    # stations, chargers
    path('api/', include('bookings.urls')),    # bookings
    path('api/payments/', include('payments.urls')),
    path('api/', include('history.urls')),     # history

    path('docs/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
]