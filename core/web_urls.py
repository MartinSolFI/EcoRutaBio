from django.urls import path
from . import web_views

urlpatterns = [
    path("", web_views.landing, name="landing"),
    path("registro/", web_views.registro, name="registro"),
    path("login/", web_views.login, name="login"),
    path("panel/", web_views.panel, name="panel"),
    path("personalizar-interfaz/", web_views.personalizar_interfaz, name="personalizar_interfaz"),
    path("mis-recolecciones/", web_views.mis_recolecciones, name="mis_recolecciones"),
    path("solicitudes/nueva/", web_views.nueva_solicitud, name="nueva_solicitud"),
    path("administracion/solicitudes/", web_views.administrar_solicitudes, name="administrar_solicitudes"),
    path("usuarios/<int:id_usuario>/editar-rol/", web_views.editar_rol, name="editar_rol"),
    path("usuarios/crear/", web_views.crear_usuario, name="crear_usuario"),
    path("usuarios/", web_views.usuarios_funciones, name="usuarios_funciones"),
    path("usuarios/<int:id_usuario>/editar/", web_views.editar_usuario, name="editar_usuario"),
    path("logout/", web_views.logout, name="logout"),
]
