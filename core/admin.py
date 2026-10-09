from django.contrib import admin

from .models import (
    MovimientoPuntos,
    Recibo,
    Recoleccion,
    ReglaConversion,
    Ruta,
    RutaParada,
    Solicitud,
    Usuario,
)

admin.site.register(ReglaConversion)
admin.site.register(Usuario)
admin.site.register(Solicitud)
admin.site.register(Recoleccion)
admin.site.register(Recibo)
admin.site.register(MovimientoPuntos)
admin.site.register(Ruta)
admin.site.register(RutaParada)
