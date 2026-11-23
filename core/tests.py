from django.contrib.auth.hashers import check_password, make_password
from django.test import TestCase

from .models import Usuario


class UsuarioApiPasswordTests(TestCase):
    def setUp(self):
        self.admin = Usuario.objects.create(
            nombre="Administrador",
            correo="admin@example.com",
            contrasena_hash=make_password("Admin12345"),
            telefono="600000000",
            direccion="Calle Principal 1",
            rol="ADMINISTRADOR",
        )
        sesion = self.client.session
        sesion["id_usuario"] = self.admin.id_usuario
        sesion["rol"] = "ADMINISTRADOR"
        sesion.save()

    def datos_usuario(self, correo, contrasena):
        return {
            "nombre": "Usuario Nuevo",
            "correo": correo,
            "contrasena_hash": contrasena,
            "telefono": "600000001",
            "direccion": "Calle Principal 2",
            "rol": "GENERADOR",
        }

    def test_api_guarda_contrasena_con_hash(self):
        respuesta = self.client.post(
            "/api/usuarios/",
            self.datos_usuario("nuevo@example.com", "Clave12345"),
            content_type="application/json",
        )

        self.assertEqual(respuesta.status_code, 201, respuesta.content)
        creado = Usuario.objects.get(correo="nuevo@example.com")
        self.assertNotEqual(creado.contrasena_hash, "Clave12345")
        self.assertTrue(check_password("Clave12345", creado.contrasena_hash))

        ingreso = self.client.post(
            "/login/",
            {"correo": "nuevo@example.com", "contrasena": "Clave12345"},
        )
        self.assertRedirects(ingreso, "/panel/")

    def test_api_actualiza_contrasena_con_hash(self):
        creado = Usuario.objects.create(
            nombre="Usuario Existente",
            correo="existente@example.com",
            contrasena_hash=make_password("Clave12345"),
            telefono="600000002",
            direccion="Calle Principal 3",
            rol="GENERADOR",
        )

        respuesta = self.client.patch(
            f"/api/usuarios/{creado.id_usuario}/",
            {"contrasena_hash": "Otra12345"},
            content_type="application/json",
        )

        self.assertEqual(respuesta.status_code, 200, respuesta.content)
        creado.refresh_from_db()
        self.assertNotEqual(creado.contrasena_hash, "Otra12345")
        self.assertTrue(check_password("Otra12345", creado.contrasena_hash))
