# PR 2: editar datos de usuario como administrador

- Estado: texto listo; PR real pendiente porque `gh` no está instalado.
- Base: `main`
- Rama: `feature/editar-usuario`
- Commit: `b2da3bb`
- Issue relacionado: Closes #<número del issue mejora>

## Título

`feat: permitir editar datos de usuario solo como administrador`

## Descripción

Añade la ruta `usuarios/<id_usuario>/editar/` y un formulario para que el rol ADMINISTRADOR modifique `nombre`, `correo`, `telefono` y `direccion` de cualquier usuario. No permite cambiar rol, contraseña ni permisos.

La vista comprueba el rol en la sesión y lo revalida en la base de datos. Valida campos obligatorios, formato de correo, longitudes del modelo y correo único.

Se añadieron 5 pruebas `TestCase`: edición correcta, Generador rechazado, sesión con rol falso rechazada, usuario inexistente y correo duplicado. Resultado: `Ran 5 tests ... OK`.

## Instrucciones para verificarlo

1. Descargar la rama y ejecutar:
   ```powershell
   python manage.py check
   python manage.py test core.tests.EditarUsuarioTests -v 2
   ```
2. Entrar con un ADMINISTRADOR y abrir `/usuarios/`.
3. Pulsar `Editar datos` en cualquier usuario, cambiar los cuatro campos y guardar.
4. Repetir con un GENERADOR y escribir directamente la URL de edición.

## Evidencia que debo capturar

1. Terminal con `python manage.py test core.tests.EditarUsuarioTests -v 2` y el texto `Ran 5 tests ... OK`.
2. Navegador en `/usuarios/` con el enlace `Editar datos` visible solo para ADMINISTRADOR.
3. Navegador en `/usuarios/<id>/editar/` mostrando los cuatro campos.
4. Navegador con el mensaje `Datos actualizados correctamente.` y la lista `/usuarios/` con los datos cambiados.
5. Navegador con sesión de GENERADOR al abrir directamente `/usuarios/<id>/editar/`: debe redirigir a `/login/`.
