from rest_framework.routers import DefaultRouter
from .views import EventViewSet, OptionViewSet, BetViewSet

router = DefaultRouter()
router.register(r"events", EventViewSet, basename="event")
router.register(r"options", OptionViewSet, basename="option")
router.register(r"bets", BetViewSet, basename="bet")

urlpatterns = router.urls
