from rest_framework import viewsets

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
from .serializers import (
    MovimientoPuntosSerializer,
    ReciboSerializer,
    RecoleccionSerializer,
    ReglaConversionSerializer,
    RutaParadaSerializer,
    RutaSerializer,
    SolicitudSerializer,
    UsuarioSerializer,
)


class ReglaConversionViewSet(viewsets.ModelViewSet):
    queryset = ReglaConversion.objects.all()
    serializer_class = ReglaConversionSerializer


class UsuarioViewSet(viewsets.ModelViewSet):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer


class SolicitudViewSet(viewsets.ModelViewSet):
    queryset = Solicitud.objects.all()
    serializer_class = SolicitudSerializer


class RecoleccionViewSet(viewsets.ModelViewSet):
    queryset = Recoleccion.objects.all()
    serializer_class = RecoleccionSerializer


class ReciboViewSet(viewsets.ModelViewSet):
    queryset = Recibo.objects.all()
    serializer_class = ReciboSerializer


class MovimientoPuntosViewSet(viewsets.ModelViewSet):
    queryset = MovimientoPuntos.objects.all()
    serializer_class = MovimientoPuntosSerializer


class RutaViewSet(viewsets.ModelViewSet):
    queryset = Ruta.objects.all()
    serializer_class = RutaSerializer


class RutaParadaViewSet(viewsets.ModelViewSet):
    queryset = RutaParada.objects.all()
    serializer_class = RutaParadaSerializer