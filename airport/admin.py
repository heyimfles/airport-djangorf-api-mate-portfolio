from django.contrib import admin

from airport.models import (
    Airport,
    Route,
    Airplane,
    AirplaneType,
    Order,
    Flight,
    Crew,
    Ticket
)


admin.site.register(Airport)
admin.site.register(Route)
admin.site.register(Airplane)
admin.site.register(AirplaneType)
admin.site.register(Order)
admin.site.register(Flight)
admin.site.register(Crew)
admin.site.register(Ticket)

