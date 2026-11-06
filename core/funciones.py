from .models import PermisoUsuario

FUNCIONES_POR_ROL = {
    "GENERADOR": {"SOLICITAR_RECOLECCION"},
    "RECOLECTOR": {"REGISTRAR_RECOLECCIONES"},
    "ADMINISTRADOR": {"ADMIN_USUARIOS", "ADMIN_SOLICITUDES"},
}


def funciones_de(usuario):
    base = set(FUNCIONES_POR_ROL.get(usuario.rol, set()))
    if usuario.rol == "ADMINISTRADOR":
        return base
    extras = set(
        PermisoUsuario.objects.filter(usuario=usuario).values_list("funcion", flat=True)
    )
    return base | extras


def tiene_funcion(usuario, funcion):
    return funcion in funciones_de(usuario)
