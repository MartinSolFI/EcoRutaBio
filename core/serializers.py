from rest_framework import serializers

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


class ReglaConversionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReglaConversion
        fields = "__all__"


class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = "__all__"
        extra_kwargs = {"contrasena_hash": {"write_only": True}}


class SolicitudSerializer(serializers.ModelSerializer):
    class Meta:
        model = Solicitud
        fields = "__all__"


class RecoleccionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recoleccion
        fields = "__all__"


class ReciboSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recibo
        fields = "__all__"


class MovimientoPuntosSerializer(serializers.ModelSerializer):
    class Meta:
        model = MovimientoPuntos
        fields = "__all__"


class RutaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ruta
        fields = "__all__"


class RutaParadaSerializer(serializers.ModelSerializer):
    class Meta:
        model = RutaParada
        fields = "__all__"