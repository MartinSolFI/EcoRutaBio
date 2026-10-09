from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    MovimientoPuntosViewSet,
    ReciboViewSet,
    RecoleccionViewSet,
    ReglaConversionViewSet,
    RutaParadaViewSet,
    RutaViewSet,
    SolicitudViewSet,
    UsuarioViewSet,
)

router = DefaultRouter()
router.register("reglas-conversion", ReglaConversionViewSet)
router.register("usuarios", UsuarioViewSet)
router.register("solicitudes", SolicitudViewSet)
router.register("recolecciones", RecoleccionViewSet)
router.register("recibos", ReciboViewSet)
router.register("movimientos-puntos", MovimientoPuntosViewSet)
router.register("rutas", RutaViewSet)
router.register("rutas-paradas", RutaParadaViewSet)

urlpatterns = [
    path("", include(router.urls)),
]