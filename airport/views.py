from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, mixins
from django.db.models import Prefetch
import django_filters

from airport.models import (
    Airport,
    Route,
    AirplaneType,
    Airplane,
    Order,
    Flight,
    Crew,
)
from airport.serializers import (
    AirportSerializer,
    RouteSerializer,
    AirplaneTypeSerializer,
    AirplaneSerializer,
    OrderSerializer,
    FlightSerializer,
    CrewSerializer,
    RouteListSerializer,
    RouteDetailSerializer,
    AirplaneListSerializer,
    CrewListSerializer,
    FlightListSerializer,
    FlightDetailSerializer,
)


class AirportViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet
):
    queryset = Airport.objects.all()
    serializer_class = AirportSerializer


class RouteViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
    mixins.RetrieveModelMixin,
):
    queryset = Route.objects.all()

    @staticmethod
    def _params_to_ints(qs):
        return [int(str_id) for str_id in qs.split(",")]

    def get_serializer_class(self):
        if self.action == "list":
            return RouteListSerializer

        if self.action == "retrieve":
            return RouteDetailSerializer

        return RouteSerializer

    def get_queryset(self):
        queryset = self.queryset

        source = self.request.query_params.get(
            "source_city",
            None
        )
        destination = self.request.query_params.get(
            "destination_city",
            None
        )

        if source:
            source = self._params_to_ints(source)
            queryset = queryset.filter(source__id__in=source)

        if destination:
            destination = self._params_to_ints(destination)
            queryset = queryset.filter(destination__id__in=destination)

        if self.action == "list":
            return queryset.select_related()

        return queryset.distinct()


class AirplaneTypeViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet
):
    queryset = AirplaneType.objects.all()
    serializer_class = AirplaneTypeSerializer


class AirplaneViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Airplane.objects.all()

    def get_serializer_class(self):
        if self.action == "list":
            return AirplaneListSerializer

        return AirplaneSerializer

    def get_queryset(self):
        queryset = self.queryset

        airplane_id = self.request.query_params.get("id", None)

        if airplane_id:
            queryset = queryset.filter(id=airplane_id)

        if self.action == "list":
            return queryset.select_related()

        return queryset.distinct()


class OrderViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet
):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def get_queryset(self):
        queryset = self.queryset.filter(
            user=self.request.user
        )

        if self.action == "list":
            return queryset.select_related()

        return queryset

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class FlightFilter(django_filters.FilterSet):
    route_source = django_filters.CharFilter(
        lookup_expr="icontains"
    )
    route_destination = django_filters.CharFilter(
        lookup_expr="icontains"
    )
    departure_time = django_filters.DateFromToRangeFilter()

    class Meta:
        model = Flight
        fields = [
            "route_source",
            "route_destination",
            "departure_time",
        ]


class FlightViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
    mixins.RetrieveModelMixin,
):
    queryset = Flight.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_class = FlightFilter

    def get_serializer_class(self):
        if self.action == "list":
            return FlightListSerializer

        if self.action == "retrieve":
            return FlightDetailSerializer

        return FlightSerializer

    def get_queryset(self):
        queryset = self.queryset

        if self.action == "list":
            return queryset.select_related()

        return queryset


class CrewViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet
):
    queryset = Crew.objects.all()

    def get_serializer_class(self):
        if self.action == "list":
            return CrewListSerializer

        return CrewSerializer

    def get_queryset(self):
        queryset = self.queryset

        if self.action == "list":
            flight_qs = Flight.objects.select_related(
                "route",
                "route__source",
                "route__destination",
                "airplane",
                "airplane__airplane_type"
            )
            queryset = queryset.prefetch_related(
                Prefetch(
                    "flight",
                    queryset=flight_qs,
                    )
                )

        return queryset
