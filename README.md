# EcoRutaBio

Backend del proyecto EcoRutaBio hecho con Django 5.2 y Django REST Framework.

**Versión actual:** `v1.1.0` (tag anotado subido a GitHub).

## Requisitos

- Python 3.11
- Git
- Dependencias de `requirements.txt`

## Instalación (PowerShell)

```powershell
git clone https://github.com/MartinSolFI/EcoRutaBio.git
cd EcoRutaBio
python -m venv venv
.\venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

Crea un archivo `.env` en la raíz con las variables usadas por `ecobackend/settings.py`:

```text
SECRET_KEY=<valor secreto>
DEBUG=False
ALLOWED_HOSTS=<dominios permitidos separados por coma>
```

Luego:

```powershell
python manage.py migrate
python manage.py check
python manage.py test
python manage.py createsuperuser
python manage.py runserver
```

## Uso

- Web: http://127.0.0.1:8000/
- Login: http://127.0.0.1:8000/login/
- Panel: http://127.0.0.1:8000/panel/
- API: http://127.0.0.1:8000/api/
- Admin: http://127.0.0.1:8000/admin/

La API usa la sesión iniciada en la web para aplicar permisos por rol.

## Funcionalidades principales

- Registro e inicio de sesión con contraseña cifrada.
- Panel por rol: GENERADOR, RECOLECTOR y ADMINISTRADOR.
- Solicitudes de recolección, asignación de rutas y registro de recolectas.
- Movimientos de EcoPuntos y recibos.
- Administración de usuarios: crear, cambiar roles, asignar funciones y editar datos.
- Edición de `nombre`, `correo`, `telefono` y `direccion` disponible solo para ADMINISTRADOR desde `/usuarios/<id>/editar/`.
- Personalización de las etiquetas del menú por ADMINISTRADOR desde `/personalizar-interfaz/`.
- Las contraseñas enviadas por la API se guardan con hash desde `v1.1.0`.

## Endpoints de la API

- `/api/reglas-conversion/`
- `/api/usuarios/`
- `/api/solicitudes/`
- `/api/recolecciones/`
- `/api/recibos/`
- `/api/movimientos-puntos/`
- `/api/rutas/`
- `/api/rutas-paradas/`

## Rutas web principales

- `/` landing
- `/registro/`
- `/login/`
- `/panel/`
- `/personalizar-interfaz/`
- `/solicitudes/nueva/`
- `/mis-recolecciones/`
- `/administracion/solicitudes/`
- `/usuarios/`
- `/usuarios/crear/`
- `/usuarios/<id>/editar-rol/`
- `/usuarios/<id>/editar/`
- `/logout/`

## Estructura

- `core/models.py`: modelos, incluido `PermisoUsuario`
- `core/serializers.py`: serializers de la API
- `core/views.py`: ViewSets de la API y permisos por rol
- `core/urls.py`: URLs de la API
- `core/web_views.py`: vistas web
- `core/web_urls.py`: URLs web
- `core/tests.py`: pruebas automáticas (`django.test.TestCase`)
- `ecobackend/settings.py`: configuración del proyecto

## Documentación del proceso

- `docs/DEUDA_TECNICA.md`: diagnóstico de deuda técnica
- `docs/issues/`: borradores de issues
- `docs/pr/`: textos de Pull Request y evidencia a capturar
- `CONTRIBUTING.md`: reglas de trabajo y commits
- `CHANGELOG.md`: historial de versiones
- `docs/EVIDENCIAS.md`: trazabilidad completa (se completará en la fase final)
