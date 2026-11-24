# Issue: editar datos de usuario como ADMINISTRADOR

- Tipo: Mejora
- Título: Permitir que ADMINISTRADOR edite nombre, correo, teléfono y dirección de cualquier usuario
- Prioridad: Media
- Responsable: sin asignar
- Número: pendiente de asignar al crear el issue
- Relación: funcionalidad prevista en el trabajo sin guardar de la fase 0

## Descripción

La web permite crear usuarios (`core/web_views.py:432`), cambiar roles (`core/web_views.py:384`) y asignar funciones (`core/web_views.py:510`), pero no editar los datos personales de un usuario ya creado. Se necesita una pantalla de edición disponible solo para el rol ADMINISTRADOR.

## Alcance

- Ruta: `usuarios/<id_usuario>/editar/`.
- Campos editables: `nombre`, `correo`, `telefono` y `direccion` (`core/models.py:21-27`).
- No se permite cambiar rol, contraseña ni permisos desde esta pantalla.
- Validar correo con formato válido, correo único, campos obligatorios y longitudes del modelo.

## Criterio para darlo por solucionado

- Un ADMINISTRADOR puede abrir el formulario y guardar cambios en los cuatro campos.
- Otro rol o una sesión sin sesión no puede acceder: es redirigido a `login`.
- Un usuario inexistente no produce error 500.
- Un correo repetido muestra error y no modifica la base de datos.
- Existen pruebas `django.test.TestCase` para admin, no admin, usuario inexistente y correo duplicado.
- `python manage.py check` y `python manage.py test` terminan sin errores.
