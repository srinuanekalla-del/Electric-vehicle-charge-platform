from rest_framework.routers import DefaultRouter
from .views import ChargerViewSet, ChargingStationViewSet

router = DefaultRouter()
router.register(r"stations", ChargingStationViewSet, basename="station")
router.register(r"chargers", ChargerViewSet, basename="charger")

urlpatterns = router.urls
