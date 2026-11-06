from uuid import uuid4
from django.utils import timezone
from rest_framework import viewsets
from django.shortcuts import get_object_or_404

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

from .permissions import PermisosPorRol


ADMIN = {"ADMINISTRADOR"}
CLIENTE = {"GENERADOR"}
RECOLECTOR = {"RECOLECTOR"}
TODOS = ADMIN | CLIENTE | RECOLECTOR


class BaseSeguroViewSet(viewsets.ModelViewSet):
    permission_classes = [PermisosPorRol]

    def usuario_actual(self):
        return self.request.ecoruta_usuario


class ReglaConversionViewSet(BaseSeguroViewSet):
    queryset = ReglaConversion.objects.all()
    serializer_class = ReglaConversionSerializer

    roles_por_accion = {
        "list": TODOS,
        "retrieve": TODOS,
        "create": ADMIN,
        "update": ADMIN,
        "partial_update": ADMIN,
        "destroy": ADMIN,
    }


class UsuarioViewSet(BaseSeguroViewSet):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer

    roles_por_accion = {
        "list": TODOS,
        "retrieve": TODOS,
        "create": ADMIN,
        "update": ADMIN,
        "partial_update": ADMIN,
        "destroy": ADMIN,
    }

    def get_queryset(self):
        usuario = self.usuario_actual()

        if usuario.rol == "ADMINISTRADOR":
            return Usuario.objects.all()

        return Usuario.objects.filter(id_usuario=usuario.id_usuario)


class SolicitudViewSet(BaseSeguroViewSet):
    queryset = Solicitud.objects.all()
    serializer_class = SolicitudSerializer

    roles_por_accion = {
        "list": TODOS,
        "retrieve": TODOS,
        "create": ADMIN | CLIENTE,
        "update": ADMIN,
        "partial_update": ADMIN,
        "destroy": ADMIN,
    }

    def get_queryset(self):
        usuario = self.usuario_actual()

        if usuario.rol == "ADMINISTRADOR":
            return Solicitud.objects.select_related("generador").all()

        if usuario.rol == "GENERADOR":
            return Solicitud.objects.filter(
                generador=usuario
            ).select_related("generador")

        return Solicitud.objects.filter(
            ruta_parada__ruta__recolector=usuario
        ).select_related("generador").distinct()

    def perform_create(self, serializer):
        usuario = self.usuario_actual()

        if usuario.rol == "GENERADOR":
            serializer.save(
                generador=usuario,
                estado="PENDIENTE",
                codigo_qr=uuid4().hex.upper(),
                fecha_solicitud=timezone.now(),
            )
        else:
            serializer.save()


class RecoleccionViewSet(BaseSeguroViewSet):
    queryset = Recoleccion.objects.all()
    serializer_class = RecoleccionSerializer

    roles_por_accion = {
        "list": TODOS,
        "retrieve": TODOS,
        "create": ADMIN,
        "update": ADMIN,
        "partial_update": ADMIN,
        "destroy": ADMIN,
    }

    def get_queryset(self):
        usuario = self.usuario_actual()

        if usuario.rol == "ADMINISTRADOR":
            return Recoleccion.objects.all()

        if usuario.rol == "GENERADOR":
            return Recoleccion.objects.filter(
                solicitud__generador=usuario
            )

        return Recoleccion.objects.filter(recolector=usuario)


class ReciboViewSet(BaseSeguroViewSet):
    queryset = Recibo.objects.all()
    serializer_class = ReciboSerializer

    roles_por_accion = {
        "list": ADMIN | CLIENTE,
        "retrieve": ADMIN | CLIENTE,
        "create": ADMIN,
        "update": ADMIN,
        "partial_update": ADMIN,
        "destroy": ADMIN,
    }

    def get_queryset(self):
        usuario = self.usuario_actual()

        if usuario.rol == "ADMINISTRADOR":
            return Recibo.objects.all()

        return Recibo.objects.filter(usuario=usuario)


class MovimientoPuntosViewSet(BaseSeguroViewSet):
    queryset = MovimientoPuntos.objects.all()
    serializer_class = MovimientoPuntosSerializer

    roles_por_accion = {
        "list": ADMIN | CLIENTE,
        "retrieve": ADMIN | CLIENTE,
        "create": ADMIN,
        "update": ADMIN,
        "partial_update": ADMIN,
        "destroy": ADMIN,
    }

    def get_queryset(self):
        usuario = self.usuario_actual()

        if usuario.rol == "ADMINISTRADOR":
            return MovimientoPuntos.objects.all()

        return MovimientoPuntos.objects.filter(usuario=usuario)


class RutaViewSet(BaseSeguroViewSet):
    queryset = Ruta.objects.all()
    serializer_class = RutaSerializer

    roles_por_accion = {
        "list": ADMIN | RECOLECTOR,
        "retrieve": ADMIN | RECOLECTOR,
        "create": ADMIN,
        "update": ADMIN,
        "partial_update": ADMIN,
        "destroy": ADMIN,
    }

    def get_queryset(self):
        usuario = self.usuario_actual()

        if usuario.rol == "ADMINISTRADOR":
            return Ruta.objects.all()

        return Ruta.objects.filter(recolector=usuario)


class RutaParadaViewSet(BaseSeguroViewSet):
    queryset = RutaParada.objects.all()
    serializer_class = RutaParadaSerializer

    roles_por_accion = {
        "list": ADMIN | RECOLECTOR,
        "retrieve": ADMIN | RECOLECTOR,
        "create": ADMIN,
        "update": ADMIN,
        "partial_update": ADMIN,
        "destroy": ADMIN,
    }

    def get_queryset(self):
        usuario = self.usuario_actual()

        if usuario.rol == "ADMINISTRADOR":
            return RutaParada.objects.all()

        return RutaParada.objects.filter(
            ruta__recolector=usuario
        )

def editar_rol(request, id_usuario):
    if request.session.get("rol") != "ADMINISTRADOR":
        return redirect("login")

    if request.method == "POST":
        from core.models import Usuario

        usuario = get_object_or_404(Usuario, id_usuario=id_usuario)
        nuevo_rol = request.POST.get("rol")

        roles_validos = [rol[0] for rol in Usuario.ROL_CHOICES]

        if nuevo_rol in roles_validos:
            if usuario.id_usuario == request.session.get("id_usuario"):
                return redirect("panel")

            usuario.rol = nuevo_rol
            usuario.save()

    return redirect("panel")