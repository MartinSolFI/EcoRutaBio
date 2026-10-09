# EcoRutaBio

Backend del proyecto EcoRutaBio hecho con Django y Django REST Framework.

## Requisitos
- Python 3.11
- Git

## Instalación (PowerShell)

```powershell
git clone https://github.com/MartinSolFI/EcoRutaBio.git
cd EcoRutaBio
python -m venv venv
.\venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

## Uso
- API: http://127.0.0.1:8000/api/
- Admin: http://127.0.0.1:8000/admin/

## Endpoints
- /api/reglas-conversion/
- /api/usuarios/
- /api/solicitudes/
- /api/recolecciones/
- /api/recibos/
- /api/movimientos-puntos/
- /api/rutas/
- /api/rutas-paradas/

## Estructura
- `core/models.py`: modelos de las 8 tablas
- `core/serializers.py`: serializers
- `core/views.py`: views de la API
- `core/urls.py`: URLs de la API