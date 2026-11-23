from django.contrib.auth.hashers import make_password
from django.test import TestCase
from django.urls import reverse

from .models import Usuario


class EditarUsuarioTests(TestCase):
    def setUp(self):
        self.admin = Usuario.objects.create(
            nombre="Administrador",
            correo="admin@example.com",
            contrasena_hash=make_password("Admin12345"),
            telefono="600000000",
            direccion="Calle Principal 1",
            rol="ADMINISTRADOR",
        )
        self.generador = Usuario.objects.create(
            nombre="Generador Original",
            correo="generador@example.com",
            contrasena_hash=make_password("Clave12345"),
            telefono="600000001",
            direccion="Calle Principal 2",
            rol="GENERADOR",
        )
        self.otro = Usuario.objects.create(
            nombre="Otro Usuario",
            correo="otro@example.com",
            contrasena_hash=make_password("Clave12345"),
            telefono="600000002",
            direccion="Calle Principal 3",
            rol="RECOLECTOR",
        )

    def iniciar_sesion(self, usuario, rol=None):
        sesion = self.client.session
        sesion["id_usuario"] = usuario.id_usuario
        sesion["nombre"] = usuario.nombre
        sesion["rol"] = rol or usuario.rol
        sesion.save()

    def url_editar(self, usuario):
        return reverse("editar_usuario", args=[usuario.id_usuario])

    def test_administrador_puede_editar_datos(self):
        self.iniciar_sesion(self.admin)
        url = self.url_editar(self.generador)

        respuesta = self.client.get(url)
        self.assertEqual(respuesta.status_code, 200)
        self.assertContains(respuesta, "Editar usuario")

        hash_original = self.generador.contrasena_hash
        rol_original = self.generador.rol

        respuesta = self.client.post(url, {
            "nombre": "Generador Editado",
            "correo": "editado@example.com",
            "telefono": "699999999",
            "direccion": "Calle Nueva 9",
        })

        self.assertEqual(respuesta.status_code, 200)
        self.assertContains(respuesta, "Datos actualizados correctamente.")

        self.generador.refresh_from_db()
        self.assertEqual(self.generador.nombre, "Generador Editado")
        self.assertEqual(self.generador.correo, "editado@example.com")
        self.assertEqual(self.generador.telefono, "699999999")
        self.assertEqual(self.generador.direccion, "Calle Nueva 9")
        self.assertEqual(self.generador.rol, rol_original)
        self.assertEqual(self.generador.contrasena_hash, hash_original)

    def test_generador_no_puede_editar(self):
        self.iniciar_sesion(self.generador)
        url = self.url_editar(self.otro)

        self.assertRedirects(self.client.get(url), "/login/")
        self.assertRedirects(self.client.post(url, {
            "nombre": "Cambio indebido",
            "correo": "cambio@example.com",
            "telefono": "600000009",
            "direccion": "Calle Falsa 9",
        }), "/login/")

        self.otro.refresh_from_db()
        self.assertEqual(self.otro.nombre, "Otro Usuario")

    def test_sesion_con_rol_falso_no_puede_editar(self):
        self.iniciar_sesion(self.generador, rol="ADMINISTRADOR")

        respuesta = self.client.get(self.url_editar(self.otro))

        self.assertRedirects(respuesta, "/login/")

    def test_usuario_inexistente_redirige(self):
        self.iniciar_sesion(self.admin)

        respuesta = self.client.get(reverse("editar_usuario", args=[999999]))

        self.assertRedirects(respuesta, "/usuarios/")

    def test_correo_duplicado_muestra_error(self):
        self.iniciar_sesion(self.admin)
        url = self.url_editar(self.generador)

        respuesta = self.client.post(url, {
            "nombre": "Generador Editado",
            "correo": "otro@example.com",
            "telefono": "600000001",
            "direccion": "Calle Principal 2",
        })

        self.assertEqual(respuesta.status_code, 200)
        self.assertContains(respuesta, "Ese correo ya lo usa otro usuario.")

        self.generador.refresh_from_db()
        self.assertEqual(self.generador.correo, "generador@example.com")
