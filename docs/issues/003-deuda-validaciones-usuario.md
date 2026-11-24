# Issue: validaciones de usuario duplicadas

- Tipo: Deuda técnica
- Título: Unificar las validaciones de usuario repetidas en registro, creación y edición
- Prioridad: Media
- Responsable: sin asignar
- Número: pendiente de asignar al crear el issue
- Relación: deuda D-03 de `docs/DEUDA_TECNICA.md`

## Descripción

La validación de datos de usuario está repetida en tres flujos:

- Registro: `core/web_views.py:19-51`.
- Creación por administrador: `core/web_views.py:432-528`.
- Edición por administrador: `core/web_views.py:595-668` (trabajo sin guardar detectado en la fase 0).

Cada sitio repite comprobaciones de campos obligatorios, formato de correo, longitudes y correo duplicado. Si se corrige una regla en un lugar, los otros dos pueden quedar desactualizados.

## Criterio para darlo por solucionado

- Existe una única función, formulario o serializador de validación reutilizado por los tres flujos.
- Los tres flujos muestran los mismos mensajes ante el mismo error.
- Las reglas actuales (longitudes del modelo y correo único) no cambian.
- Hay pruebas que cubren los tres flujos.
- `python manage.py check` y `python manage.py test` terminan sin errores.
