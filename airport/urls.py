from django.urls import path, include
from rest_framework import routers

from airport.views import (
    AirportViewSet,
    RouteViewSet,
    AirplaneTypeViewSet,
    AirplaneViewSet,
    OrderViewSet,
    FlightViewSet,
    CrewViewSet,
    TicketViewSet,
)


router = routers.DefaultRouter()
router.register("airport", AirportViewSet)
router.register("route", RouteViewSet)
router.register("airplane_type", AirplaneTypeViewSet)
router.register("airplane", AirplaneViewSet)
router.register("order", OrderViewSet)
router.register("flight", FlightViewSet)
router.register("crew", CrewViewSet)
router.register("ticket", TicketViewSet)

urlpatterns = [
    path("", include(router.urls)),
]

app_name = "airport"
