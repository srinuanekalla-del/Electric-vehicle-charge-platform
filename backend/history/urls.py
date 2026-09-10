from rest_framework.routers import DefaultRouter
from .views import ChargingHistoryViewSet

router = DefaultRouter()
router.register(r"history", ChargingHistoryViewSet, basename="history")
urlpatterns = router.urls
