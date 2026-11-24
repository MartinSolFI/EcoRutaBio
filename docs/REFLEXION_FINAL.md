# Reflexión final

## Estado inicial

El proyecto tenía una base funcional, pero con deuda técnica clara: contraseñas guardadas sin cifrar desde la API, cero pruebas automáticas y validaciones de usuario repetidas. El diagnóstico se ordenó en `docs/DEUDA_TECNICA.md` con diez entradas priorizadas, de las cuales se atendieron D-01 y parte de D-03/D-10 durante el proceso.

## Trabajo realizado

Se trabajó con ramas separadas para cada cambio: `fix/api-password-hash` y `feature/editar-usuario`, integradas después en `main` mediante el merge `626afb2` y etiquetadas como `v1.1.0`. Posteriormente, en `login-roles`, se consolidaron los arreglos, la personalización de interfaz, las pruebas y la documentación en el commit `3237421`.

Los cambios reales implementados fueron:

1. Hash de contraseñas en `create()` y `update()` del serializador de usuarios, con pruebas que demuestran que el usuario puede iniciar sesión después de ser creado por la API.
2. Edición de datos de usuario restringida a ADMINISTRADOR, con revalidación del rol en base de datos.
3. Personalización de etiquetas del menú, con un único diccionario de valores por defecto reutilizado por el panel y el formulario.

## Aprendizajes

- La trazabilidad no es solo guardar comandos: requiere conectar deuda → issue → rama → commit → PR → evidencia.
- Las pruebas automáticas fueron el mecanismo que permitió comprobar que los arreglos no rompían login, roles ni edición; el total pasó de 0 a 12 pruebas.
- Centralizar las etiquetas evitó que el panel y el formulario se desactualizaran por separado.
- Documentar entorno y variables (`SECRET_KEY`, `venv`) ahorró tiempo al reproducir fallos que parecían del código.

## Pendiente y siguiente paso

Quedan por cerrar los números reales de issues y Pull Request en GitHub, las capturas de navegador y la deuda D-03 (validaciones de usuario aún duplicadas). La versión publicada sigue siendo `v1.1.0`; el trabajo posterior está registrado como `Unreleased` en `CHANGELOG.md`.

En conjunto, el repositorio muestra el proceso completo: diagnóstico, ramas, cambios verificados, documentación y evidencia reproducible.
