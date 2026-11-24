# Changelog

Todos los cambios notables se documentan en este archivo.

El formato sigue [Keep a Changelog](https://keepachangelog.com/es-ES/1.1.0/) y el proyecto usa [SemVer](https://semver.org/lang/es/).

## [Unreleased]

### Added

- Personalización de etiquetas del menú desde `/personalizar-interfaz/`, solo para ADMINISTRADOR, con valores por defecto y persistencia en `TextoInterfaz` (migración `0004_textointerfaz`).
- 5 pruebas automáticas nuevas para personalización de interfaz; el total de pruebas del proyecto sube a 12.

### Changed

- Las etiquetas por defecto del menú se definen una sola vez en `core/web_views.py` y se reutilizan en el panel y en el formulario.

### Fixed

- El enlace "Mis EcoPuntos" y el de personalización muestran el texto configurado en lugar de uno fijo.

## [1.1.0] - 2026-11-23

### Added

- Edición de `nombre`, `correo`, `telefono` y `direccion` de cualquier usuario, disponible solo para el rol ADMINISTRADOR en `/usuarios/<id>/editar/` (rama `feature/editar-usuario`, commit `b2da3bb`).
- 7 pruebas automáticas con `django.test.TestCase`: 2 para contraseñas de la API y 5 para edición de usuarios.

### Fixed

- Las contraseñas creadas o actualizadas mediante `POST/PATCH /api/usuarios/` ahora se guardan con `make_password` en lugar de texto plano (rama `fix/api-password-hash`, commit `a108a81`).
- Conflicto de `core/tests.py` resuelto al integrar ambas ramas en el merge `626afb2`.

### Security

- Se evita que las credenciales enviadas por la API queden almacenadas sin cifrar.

## [1.0.0] - 2026-11-23

### Added

- Landing, login, registro, panel y permisos por usuario (commit `e8221d3`).
- ViewSets y rutas de la API para reglas de conversión, usuarios, solicitudes, recolecciones, recibos, movimientos de puntos, rutas y paradas.
- Modelo `PermisoUsuario` y migraciones `0002_solicitud_tipo_material` y `0003_permiso_usuario`.

[1.1.0]: https://github.com/MartinSolFI/EcoRutaBio/releases/tag/v1.1.0
[1.0.0]: https://github.com/MartinSolFI/EcoRutaBio/releases/tag/v1.0.0
