from rest_framework.permissions import BasePermission

from .models import Usuario


class PermisosPorRol(BasePermission):
    """
    Comprueba el rol real del usuario consultando la base de datos.
    Cada ViewSet define los roles permitidos para cada acción.
    """

    def has_permission(self, request, view):
        id_usuario = request.session.get("id_usuario")

        if not id_usuario:
            return False

        usuario = Usuario.objects.filter(
            id_usuario=id_usuario
        ).first()

        if not usuario:
            return False

        request.ecoruta_usuario = usuario

        permisos = getattr(view, "roles_por_accion", {})
        accion = getattr(view, "action", None)

        roles_permitidos = permisos.get(accion, set())

        return usuario.rol in roles_permitidos