# Evidencias y trazabilidad

Fecha de revisión: 2026-11-23.

Este documento reúne la evidencia verificable del proceso. No incluye números de issue/PR ni capturas inventadas: donde aún no existen, se indica como pendiente.

## Entorno verificado

- Windows, PowerShell, Python 3.11, entorno virtual `venv/`.
- Django 5.2.18 (`requirements.txt`).
- Repositorio: `https://github.com/MartinSolFI/EcoRutaBio.git`.

## Cambios y su evidencia

| Cambio | Commit / tag | Rama | Documento relacionado |
|--------|--------------|------|-----------------------|
| Landing, login, registro, roles y permisos | `e8221d3`, tag `v1.0.0` (2026-11-06) | `login-roles` | `README.md`, `docs/DEUDA_TECNICA.md` |
| Hash de contraseñas creadas/actualizadas por la API | `a108a81` (2026-11-23) | `fix/api-password-hash` | `docs/issues/001-bug-api-contrasena-sin-hash.md`, `docs/pr/001-fix-api-contrasena-sin-hash.md` |
| Edición de datos de usuario solo para ADMINISTRADOR | `b2da3bb` (2026-11-23) | `feature/editar-usuario` | `docs/issues/002-mejora-editar-usuario-admin.md`, `docs/pr/002-feature-editar-usuario-admin.md` |
| Integración en la rama estable | `626afb2` (2026-11-23), tag `v1.1.0` | `main` | `CHANGELOG.md` |
| Unificar validaciones de usuario (deuda D-03) | Sin implementar | Sin rama | `docs/issues/003-deuda-validaciones-usuario.md` |

`v1.1.0` apunta al commit de merge `626afb2`. `main` está alineada con `origin/main`.

## Verificación ejecutada en `main`

Para no modificar el árbol de trabajo se exportó `main` con `git archive --format=zip -o ... main` a una carpeta temporal y se ejecutaron los comandos con el intérprete de `venv`:

```text
$env:SECRET_KEY = "<valor de prueba local>"
& .\venv\Scripts\python.exe manage.py check
System check identified no issues (0 silenced).

& .\venv\Scripts\python.exe manage.py test -v 1
Found 7 test(s).
Ran 7 tests in 22.855s
OK
```

Las 7 pruebas son 2 de `UsuarioApiPasswordTests` y 5 de `EditarUsuarioTests`, de acuerdo con `CHANGELOG.md` y los textos de `docs/pr/`.

### Condiciones necesarias para reproducirlo

- Usar `venv\Scripts\python.exe`: con el Python global falla `ModuleNotFoundError: No module named 'whitenoise'`, aunque `whitenoise==6.12.0` está en `requirements.txt`.
- Definir `SECRET_KEY`: sin ella, las pruebas que usan sesión fallan con `ImproperlyConfigured: The SECRET_KEY setting must not be empty.` Esto confirma la deuda D-06 de `docs/DEUDA_TECNICA.md`.
- El valor de `SECRET_KEY` usado fue solo de prueba local; no se guardó en el repositorio.

## Verificación en la rama de trabajo `login-roles`

La rama activa partió de `e8221d3`. Para dejarla verificable se incorporaron en el árbol, sin hacer merge, los arreglos que `main` tenía en `a108a81` y `b2da3bb`, además de la funcionalidad "Personalizar interfaz" (`TextoInterfaz`, migración `0004_textointerfaz`, vista, plantilla y enlace en el panel). Todo queda registrado en un único commit nuevo.

```text
& .\venv\Scripts\python.exe manage.py check
System check identified no issues (0 silenced).

& .\venv\Scripts\python.exe manage.py makemigrations --check --dry-run
No changes detected

& .\venv\Scripts\python.exe manage.py test -v 1
Found 12 test(s).
Ran 12 tests in 37.349s
OK
```

Las 12 pruebas se reparten en 2 de API, 5 de edición de usuarios y 5 nuevas de personalización de interfaz (guardado y reflejo en el panel, valor vacío, texto largo, acceso de Generador y valores por defecto). No se hizo merge, push ni tag durante esta revisión.

## Evidencia pendiente

- Crear los issues y PR reales para obtener sus números; los borradores usan marcadores `Closes #<número>`. La CLI `gh` no está instalada y no hay sesión autenticada en esta revisión.
- Capturas de navegador indicadas en `docs/pr/001-fix-api-contrasena-sin-hash.md` y `docs/pr/002-feature-editar-usuario-admin.md`: no capturadas en esta revisión. Las salidas de terminal sí quedan registradas como texto en este documento.
