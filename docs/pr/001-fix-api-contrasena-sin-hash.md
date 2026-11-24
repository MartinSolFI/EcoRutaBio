# PR 1: arreglar contraseñas sin hash en la API

- Estado: texto listo; PR real pendiente porque `gh` no está instalado.
- Base: `main`
- Rama: `fix/api-password-hash`
- Commit: `a108a81`
- Issue relacionado: Closes #<número del issue bug>

## Título

`fix: aplicar hash a contraseñas creadas o actualizadas por la API`

## Descripción

`UsuarioSerializer` guardaba directamente el valor recibido en `contrasena_hash`. Como la web valida con `check_password`, los usuarios creados por `POST /api/usuarios/` no podían iniciar sesión y su contraseña quedaba en texto plano.

Ahora `create()` y `update()` aplican `make_password` antes de guardar. Se añadieron dos pruebas `TestCase`: una para creación y otra para actualización.

Antes del arreglo, las pruebas fallaron con:

```text
AssertionError: 'Clave12345' == 'Clave12345'
AssertionError: 'Otra12345' == 'Otra12345'
FAILED (failures=2)
```

Después del arreglo: `Ran 2 tests ... OK`.

## Instrucciones para verificarlo

1. Descargar la rama y ejecutar:
   ```powershell
   python manage.py check
   python manage.py test core.tests.UsuarioApiPasswordTests -v 2
   ```
2. Crear un usuario desde `POST /api/usuarios/` con una sesión de ADMINISTRADOR.
3. Comprobar el hash guardado:
   ```powershell
   python manage.py shell -c "from core.models import Usuario; u=Usuario.objects.get(correo='nuevo@example.com'); print(u.contrasena_hash[:20])"
   ```
4. Iniciar sesión en `/login/` con ese correo y contraseña.

## Evidencia que debo capturar

1. Terminal con `python manage.py test core.tests.UsuarioApiPasswordTests -v 2` y el texto `Ran 2 tests ... OK`.
2. Terminal con el `print` del hash: debe empezar con `pbkdf2_sha256$`, nunca con la contraseña escrita.
3. Navegador mostrando el panel `/panel/` después de iniciar sesión con el usuario creado desde la API.
