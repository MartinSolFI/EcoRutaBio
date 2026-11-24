# Cómo contribuir a EcoRutaBio

## Ramas

- `main`: rama estable. Solo recibe cambios revisados y lleva los tags de versión.
- `feature/*`: cambios nuevos. Se crean desde `main`. Ejemplo: `feature/editar-usuario`.
- `fix/*`: correcciones de bugs. Se crean desde `main`. Ejemplo: `fix/api-password-hash`.

Un cambio por rama. No mezclar una mejora y un bug en la misma rama.

## Formato de commits

Usa un prefijo y un mensaje corto en español:

- `feat:` nueva funcionalidad
- `fix:` corrección de bug
- `refactor:` reorganización sin cambiar comportamiento
- `docs:` documentación
- `test:` pruebas

Ejemplos reales del repositorio:

```text
fix: aplicar hash a contraseñas creadas o actualizadas por la API
feat: permitir editar datos de usuario solo como administrador
```

## Antes de abrir un Pull Request

1. Ejecutar:

```powershell
python manage.py check
python manage.py test
```

2. Añadir solo archivos concretos:

```powershell
git add core/serializers.py core/tests.py
```

Nunca usar `git add .`, `git push --force` ni `git reset --hard`.

3. No subir: `core/arboles.py`, `respaldo_web/`, `core_ecorutabio.zip`, `db.sqlite3`, `.env`, `venv/` ni copias `.respaldo` o `.antes_*`.

## Pull Requests

- Un PR por cambio, con `main` como base.
- Título descriptivo y prefijo del commit principal.
- Descripción qué cambia y por qué.
- Referencia al issue con `Closes #N` cuando el número real exista.
- Instrucciones para verificarlo.
- Evidencia: comandos y capturas de pantallas indicadas en `docs/pr/`.

La CLI `gh` no está instalada en este equipo, así que los textos de PR se guardan en `docs/pr/` hasta que se creen a mano.

## Reglas básicas

- Trabajar una fase a la vez y esperar confirmación antes de seguir.
- Pedir permiso antes de `push`, `merge`, tags, issues o PR.
- No inventar nombres, números de issue/PR ni fechas.
- Si un comando falla, detenerse y explicar el error antes de continuar.
- Escribir respuestas y documentación en español, de forma simple y breve.
