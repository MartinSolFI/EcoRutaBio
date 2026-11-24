# Issue: contraseñas sin hash en la API

- Tipo: Bug
- Título: La API guarda contraseñas sin hash y el usuario creado no puede iniciar sesión
- Prioridad: Alta
- Responsable: sin asignar
- Número: pendiente de asignar al crear el issue
- Relación: deuda D-01 de `docs/DEUDA_TECNICA.md`

## Descripción

`UsuarioSerializer` (`core/serializers.py:21-25`) expone todos los campos y solo marca `contrasena_hash` como `write_only`, pero no transforma su valor. `UsuarioViewSet` permite `create` al rol ADMINISTRADOR (`core/views.py:58-69`). En cambio, el login web valida con `check_password` (`core/web_views.py:71`), que espera un hash de Django.

## Pasos para reproducirlo

1. Entrar con una sesión de ADMINISTRADOR.
2. Enviar `POST /api/usuarios/` con `nombre`, `correo`, `contrasena_hash`, `telefono`, `direccion` y `rol`.
3. Revisar el valor guardado en `contrasena_hash` e intentar iniciar sesión con ese correo y contraseña.

## Resultado actual

La contraseña queda guardada como texto plano y el inicio de sesión falla.

## Resultado esperado

La contraseña se guarda con `make_password` y el usuario puede iniciar sesión normalmente.

## Criterio para darlo por solucionado

- Existe una prueba `django.test.TestCase` que demuestra el fallo antes del arreglo.
- La misma prueba pasa después de aplicar hash en `create()` y `update()` del serializador.
- Ningún campo `contrasena_hash` queda almacenado en texto plano.
- `python manage.py check` y `python manage.py test` terminan sin errores.
