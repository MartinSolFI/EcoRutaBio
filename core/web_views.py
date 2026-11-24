from .funciones import FUNCIONES_POR_ROL, funciones_de, tiene_funcion
from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password, check_password
from django.views.decorators.http import require_http_methods
from django.db.models import Sum, Count
from django.utils import timezone

from .models import (
    Usuario, Solicitud, Recoleccion, Recibo,
    MovimientoPuntos, ReglaConversion, Ruta, RutaParada, TextoInterfaz
)


ETIQUETAS_INTERFAZ = {
    "inicio": "Inicio",
    "mis_solicitudes": "Mis solicitudes",
    "mis_ecopuntos": "Mis EcoPuntos",
    "mis_recibos": "Mis recibos",
    "solicitar_recoleccion": "Solicitar recoleccion",
    "mis_rutas": "Mis rutas",
    "recolecciones": "Recolecciones",
    "usuarios": "Usuarios",
    "solicitudes": "Solicitudes",
    "administrar_solicitudes": "Administrar solicitudes",
    "administracion": "Administracion",
    "administrar_usuarios": "Administrar usuarios",
    "personalizar_interfaz": "Personalizar interfaz",
    "cerrar_sesion": "Cerrar sesion",
}


def landing(request):
    return render(request, "core/landing.html")


@require_http_methods(["GET", "POST"])
def registro(request):
    if request.method == "POST":
        nombre = request.POST.get("nombre", "").strip()
        correo = request.POST.get("correo", "").strip().lower()
        telefono = request.POST.get("telefono", "").strip()
        direccion = request.POST.get("direccion", "").strip()
        contrasena = request.POST.get("contrasena", "")
        confirmar = request.POST.get("confirmar", "")

        if not all([nombre, correo, telefono, direccion, contrasena]):
            return render(request, "core/registro.html",
                          {"error": "Completa todos los campos."})

        if contrasena != confirmar:
            return render(request, "core/registro.html",
                          {"error": "Las contraseñas no coinciden."})

        if len(contrasena) < 8:
            return render(request, "core/registro.html",
                          {"error": "Mínimo 8 caracteres."})

        if Usuario.objects.filter(correo__iexact=correo).exists():
            return render(request, "core/registro.html",
                          {"error": "Este correo ya está registrado."})

        usuario = Usuario.objects.create(
            nombre=nombre,
            correo=correo,
            contrasena_hash=make_password(contrasena),
            telefono=telefono,
            direccion=direccion,
            rol="GENERADOR"
        )

        request.session.cycle_key()
        request.session["id_usuario"] = usuario.id_usuario
        request.session["nombre"] = usuario.nombre
        request.session["rol"] = usuario.rol

        return redirect("panel")

    return render(request, "core/registro.html")


@require_http_methods(["GET", "POST"])
def login(request):
    if request.method == "POST":
        correo = request.POST.get("correo", "").strip().lower()
        contrasena = request.POST.get("contrasena", "")

        usuario = Usuario.objects.filter(correo__iexact=correo).first()

        if usuario and check_password(contrasena, usuario.contrasena_hash):
            request.session.cycle_key()
            request.session["id_usuario"] = usuario.id_usuario
            request.session["nombre"] = usuario.nombre
            request.session["rol"] = usuario.rol
            return redirect("panel")

        return render(request, "core/login.html",
                      {"error": "Correo o contraseña incorrectos."})

    return render(request, "core/login.html")


def panel(request):
    id_usuario = request.session.get("id_usuario")

    if not id_usuario:
        return redirect("login")

    usuario = Usuario.objects.filter(id_usuario=id_usuario).first()

    if not usuario:
        request.session.flush()
        return redirect("login")

    contexto = {"usuario": usuario}

    personalizados = dict(
        TextoInterfaz.objects.values_list("clave", "texto")
    )
    contexto["textos"] = {
        clave: personalizados.get(clave, defecto)
        for clave, defecto in ETIQUETAS_INTERFAZ.items()
    }

    if usuario.rol == "GENERADOR":
        solicitudes = Solicitud.objects.filter(
            generador=usuario
        ).order_by("-fecha_solicitud")

        acumulados = MovimientoPuntos.objects.filter(
            usuario=usuario, tipo="ACUMULA"
        ).aggregate(total=Sum("cantidad"))["total"] or 0

        redimidos = MovimientoPuntos.objects.filter(
            usuario=usuario, tipo="REDIME"
        ).aggregate(total=Sum("cantidad"))["total"] or 0

        contexto.update({
            "solicitudes": solicitudes[:10],
            "total_solicitudes": solicitudes.count(),
            "pendientes": solicitudes.filter(estado="PENDIENTE").count(),
            "recolectadas": solicitudes.filter(estado="RECOLECTADA").count(),
            "puntos": acumulados - redimidos,
            "recibos": Recibo.objects.filter(usuario=usuario).order_by("-id_recibo")[:5],
        })

    elif usuario.rol == "RECOLECTOR":
        rutas = Ruta.objects.filter(
            recolector=usuario
        ).order_by("-fecha")

        contexto.update({
            "rutas": rutas,
            "total_rutas": rutas.count(),
            "paradas": RutaParada.objects.filter(
                ruta__recolector=usuario
            ).count(),
            "recolecciones": Recoleccion.objects.filter(
                recolector=usuario
            ).count(),
        })

    elif usuario.rol == "ADMINISTRADOR":
        contexto.update({
            "roles": Usuario.ROL_CHOICES,
            "total_usuarios": Usuario.objects.count(),
            "total_generadores": Usuario.objects.filter(rol="GENERADOR").count(),
            "total_recolectores": Usuario.objects.filter(rol="RECOLECTOR").count(),
            "total_solicitudes": Solicitud.objects.count(),
            "total_pendientes": Solicitud.objects.filter(estado="PENDIENTE").count(),
            "total_recolecciones": Recoleccion.objects.count(),
            "total_rutas": Ruta.objects.count(),
            "usuarios": Usuario.objects.all().order_by("-id_usuario")[:10],
            "solicitudes": Solicitud.objects.all().order_by("-fecha_solicitud")[:10],
        })

    contexto["funciones"] = funciones_de(usuario)
    return render(request, "core/panel.html", contexto)


def logout(request):
    request.session.flush()
    return redirect("landing")

def nueva_solicitud(request):
    from decimal import Decimal, InvalidOperation
    from uuid import uuid4
    from django.utils import timezone

    id_usuario = request.session.get("id_usuario")

    if not id_usuario:
        return redirect("login")

    usuario = Usuario.objects.filter(id_usuario=id_usuario).first()

    if not usuario:
        request.session.flush()
        return redirect("login")

    if not tiene_funcion(usuario, "SOLICITAR_RECOLECCION"):
        return redirect("panel")

    if request.method == "POST":
        direccion = request.POST.get("direccion", "").strip()
        peso = request.POST.get("peso_estimado", "").strip()
        franja = request.POST.get("franja_horaria", "").strip()
        material = request.POST.get("tipo_material", "").strip()

        materiales_validos = [
            "PLASTICO", "PAPEL", "CARTON",
            "VIDRIO", "METAL", "OTROS"
        ]

        franjas_validas = [
            "MAÑANA", "TARDE", "NOCHE"
        ]

        try:
            peso_decimal = Decimal(peso)
        except (InvalidOperation, ValueError):
            return render(request, "core/solicitud_nueva.html",
                          {"error": "Ingresa un peso válido."})

        if not direccion or not franja:
            return render(request, "core/solicitud_nueva.html",
                          {"error": "Completa todos los campos."})

        if peso_decimal <= 0 or peso_decimal > 100000:
            return render(request, "core/solicitud_nueva.html",
                          {"error": "El peso debe ser mayor que cero y válido."})

        if material not in materiales_validos or franja not in franjas_validas:
            return render(request, "core/solicitud_nueva.html",
                          {"error": "Selecciona opciones válidas."})

        Solicitud.objects.create(
            generador=usuario,
            direccion=direccion,
            peso_estimado=peso_decimal,
            tipo_material=material,
            franja_horaria=franja,
            codigo_qr=uuid4().hex.upper(),
            estado="PENDIENTE",
            fecha_solicitud=timezone.now()
        )

        return redirect("panel")

    return render(request, "core/solicitud_nueva.html")

def administrar_solicitudes(request):
    from django.db.models import Max

    id_usuario = request.session.get("id_usuario")
    if not id_usuario:
        return redirect("login")

    administrador = Usuario.objects.filter(id_usuario=id_usuario).first()
    if not administrador or not tiene_funcion(administrador, "ADMIN_SOLICITUDES"):
        return redirect("panel")

    mensaje = None

    if request.method == "POST":
        id_solicitud = request.POST.get("id_solicitud")
        accion = request.POST.get("accion")
        solicitud = Solicitud.objects.filter(id_solicitud=id_solicitud).first()

        if not solicitud:
            mensaje = "No se encontró la solicitud."
        elif accion == "asignar":
            if solicitud.estado != "PENDIENTE":
                mensaje = "Solo puedes asignar solicitudes pendientes."
            else:
                id_recolector = request.POST.get("recolector")
                recolector = Usuario.objects.filter(
                    id_usuario=id_recolector,
                    rol="RECOLECTOR"
                ).first()

                if not recolector:
                    mensaje = "Selecciona un recolector válido."
                else:
                    ruta, creada = Ruta.objects.get_or_create(
                        recolector=recolector,
                        fecha=timezone.localdate()
                    )

                    ultimo_orden = RutaParada.objects.filter(
                        ruta=ruta
                    ).aggregate(maximo=Max("orden"))["maximo"] or 0

                    RutaParada.objects.create(
                        ruta=ruta,
                        solicitud=solicitud,
                        orden=ultimo_orden + 1
                    )

                    solicitud.estado = "ASIGNADA"
                    solicitud.save(update_fields=["estado"])
                    mensaje = "Solicitud asignada correctamente."

        elif accion == "cancelar":
            if solicitud.estado == "PENDIENTE":
                solicitud.estado = "CANCELADA"
                solicitud.save(update_fields=["estado"])
                mensaje = "Solicitud cancelada."
            else:
                mensaje = "Solo puedes cancelar solicitudes pendientes."

    solicitudes = Solicitud.objects.select_related("generador").order_by(
        "-fecha_solicitud"
    )
    recolectores = Usuario.objects.filter(rol="RECOLECTOR").order_by("nombre")

    return render(request, "core/administrar_solicitudes.html", {
        "solicitudes": solicitudes,
        "recolectores": recolectores,
        "mensaje": mensaje,
    })

def mis_recolecciones(request):
    from decimal import Decimal, InvalidOperation
    from django.db import transaction
    from .models import ReglaConversion

    id_usuario = request.session.get("id_usuario")

    if not id_usuario:
        return redirect("login")

    usuario = Usuario.objects.filter(id_usuario=id_usuario).first()

    if not usuario:
        request.session.flush()
        return redirect("login")

    if not tiene_funcion(usuario, "REGISTRAR_RECOLECCIONES"):
        return redirect("panel")

    mensaje = None
    error = None

    if request.method == "POST":
        id_solicitud = request.POST.get("id_solicitud")
        peso = request.POST.get("peso_real", "").strip()

        try:
            peso_decimal = Decimal(peso)
        except (InvalidOperation, ValueError):
            peso_decimal = None

        parada = RutaParada.objects.filter(
            solicitud_id=id_solicitud,
            ruta__recolector=usuario
        ).select_related("solicitud").first()

        if not parada:
            error = "No se encontr\u00f3 esta asignaci\u00f3n."
        elif parada.solicitud.estado != "ASIGNADA":
            error = "Esta solicitud ya no est\u00e1 pendiente de recolecci\u00f3n."
        elif Recoleccion.objects.filter(solicitud=parada.solicitud).exists():
            error = "Esta solicitud ya fue registrada como recolectada."
        elif peso_decimal is None or peso_decimal <= 0 or peso_decimal > 100000:
            error = "Ingresa un peso real v\u00e1lido."
        else:
            regla = ReglaConversion.objects.filter(
                activa=True
            ).order_by("-vigente_desde").first()

            if not regla:
                error = "No hay una regla de conversi\u00f3n activa."
            else:
                with transaction.atomic():
                    recoleccion = Recoleccion.objects.create(
                        solicitud=parada.solicitud,
                        recolector=usuario,
                        peso_real=peso_decimal,
                        fecha_hora=timezone.now()
                    )

                    parada.solicitud.estado = "RECOLECTADA"
                    parada.solicitud.save(update_fields=["estado"])

                    MovimientoPuntos.objects.create(
                        usuario=parada.solicitud.generador,
                        recoleccion=recoleccion,
                        regla=regla,
                        tipo="ACUMULA",
                        cantidad=int(peso_decimal * regla.puntos_por_kg),
                        fecha=recoleccion.fecha_hora
                    )

                mensaje = "\u00a1Recolecci\u00f3n registrada correctamente!"

    paradas = RutaParada.objects.filter(
        ruta__recolector=usuario
    ).select_related(
        "ruta", "solicitud", "solicitud__generador"
    ).order_by("ruta__fecha", "orden")

    return render(request, "core/mis_recolecciones.html", {
        "usuario": usuario,
        "paradas": paradas,
        "mensaje": mensaje,
        "error": error,
    })


def editar_rol(request, id_usuario):
    if request.session.get("rol") != "ADMINISTRADOR":
        return redirect("login")

    if request.method != "POST":
        return redirect("panel")

    administrador = Usuario.objects.filter(
        id_usuario=request.session.get("id_usuario"),
        rol="ADMINISTRADOR"
    ).first()

    if not administrador:
        request.session.flush()
        return redirect("login")

    usuario = Usuario.objects.filter(
        id_usuario=id_usuario
    ).first()

    if not usuario:
        return redirect("panel")

    # Evitar que el administrador cambie su propio rol.
    if usuario.id_usuario == administrador.id_usuario:
        return redirect("panel")

    nuevo_rol = request.POST.get("rol")
    roles_validos = [rol[0] for rol in Usuario.ROL_CHOICES]

    if nuevo_rol not in roles_validos:
        return redirect("panel")

    # Evitar dejar el sistema sin administradores.
    if usuario.rol == "ADMINISTRADOR" and nuevo_rol != "ADMINISTRADOR":
        total_admins = Usuario.objects.filter(
            rol="ADMINISTRADOR"
        ).count()

        if total_admins <= 1:
            return redirect("panel")

    usuario.rol = nuevo_rol
    usuario.save(update_fields=["rol"])

    return redirect("panel")


def crear_usuario(request):
    from django.core.exceptions import ValidationError
    from django.core.validators import validate_email

    if request.session.get("rol") != "ADMINISTRADOR":
        return redirect("login")

    administrador = Usuario.objects.filter(
        id_usuario=request.session.get("id_usuario"),
        rol="ADMINISTRADOR"
    ).first()

    if not administrador:
        request.session.flush()
        return redirect("login")

    contexto = {"roles": Usuario.ROL_CHOICES, "datos": {}}

    if request.method == "POST":
        datos = {
            "nombre": request.POST.get("nombre", "").strip(),
            "correo": request.POST.get("correo", "").strip().lower(),
            "telefono": request.POST.get("telefono", "").strip(),
            "direccion": request.POST.get("direccion", "").strip(),
            "rol": request.POST.get("rol", ""),
        }
        contrasena = request.POST.get("contrasena", "")
        confirmar = request.POST.get("confirmar", "")
        contexto["datos"] = datos

        roles_validos = dict(Usuario.ROL_CHOICES)

        try:
            validate_email(datos["correo"])
            correo_valido = True
        except ValidationError:
            correo_valido = False

        error = None

        if not all([datos["nombre"], datos["correo"], datos["telefono"],
                    datos["direccion"], contrasena]):
            error = "Completa todos los campos."
        elif not correo_valido:
            error = "Ingresa un correo v\u00e1lido."
        elif datos["rol"] not in roles_validos:
            error = "Selecciona un rol v\u00e1lido."
        elif contrasena != confirmar:
            error = "Las contrase\u00f1as no coinciden."
        elif len(contrasena) < 8:
            error = "M\u00ednimo 8 caracteres."
        elif (len(datos["nombre"]) > 100 or len(datos["correo"]) > 120
              or len(datos["telefono"]) > 20 or len(datos["direccion"]) > 150):
            error = "Alg\u00fan campo es demasiado largo."
        elif Usuario.objects.filter(correo__iexact=datos["correo"]).exists():
            error = "Este correo ya est\u00e1 registrado."

        if error:
            contexto["error"] = error
        else:
            Usuario.objects.create(
                nombre=datos["nombre"],
                correo=datos["correo"],
                contrasena_hash=make_password(contrasena),
                telefono=datos["telefono"],
                direccion=datos["direccion"],
                rol=datos["rol"]
            )
            contexto["exito"] = (
                "Usuario creado correctamente: "
                + datos["nombre"] + " (" + roles_validos[datos["rol"]] + ")."
            )
            contexto["datos"] = {}

    return render(request, "core/crear_usuario.html", contexto)


@require_http_methods(["GET", "POST"])
def usuarios_funciones(request):
    from .models import PermisoUsuario

    id_usuario = request.session.get("id_usuario")
    if not id_usuario:
        return redirect("login")

    usuario = Usuario.objects.filter(id_usuario=id_usuario).first()
    if not usuario:
        request.session.flush()
        return redirect("login")

    if not tiene_funcion(usuario, "ADMIN_USUARIOS"):
        return redirect("panel")

    es_admin = usuario.rol == "ADMINISTRADOR"
    mensaje = None

    if request.method == "POST":
        if not es_admin:
            return redirect("usuarios_funciones")

        id_destino = request.POST.get("id_usuario", "")
        destino = None
        if id_destino.isdigit():
            destino = Usuario.objects.filter(id_usuario=id_destino).first()

        if destino and destino.rol != "ADMINISTRADOR":
            validas = {codigo for codigo, _ in PermisoUsuario.FUNCION_CHOICES}
            base = FUNCIONES_POR_ROL.get(destino.rol, set())
            marcadas = (set(request.POST.getlist("funciones")) & validas) - base
            PermisoUsuario.objects.filter(usuario=destino).exclude(
                funcion__in=marcadas
            ).delete()
            for funcion in marcadas:
                PermisoUsuario.objects.get_or_create(usuario=destino, funcion=funcion)
            mensaje = "Funciones de " + destino.nombre + " actualizadas."

    filas = []
    consulta = Usuario.objects.prefetch_related("permisos_extra").order_by("rol", "nombre")
    for u in consulta[:300]:
        base = FUNCIONES_POR_ROL.get(u.rol, set())
        extras = {p.funcion for p in u.permisos_extra.all()}
        funciones = [
            {
                "codigo": codigo,
                "nombre": nombre,
                "base": codigo in base,
                "marcada": codigo in base or codigo in extras,
            }
            for codigo, nombre in PermisoUsuario.FUNCION_CHOICES
        ]
        filas.append({"usuario": u, "funciones": funciones})

    return render(request, "core/usuarios_funciones.html", {
        "usuario": usuario,
        "es_admin": es_admin,
        "filas": filas,
        "mensaje": mensaje,
    })


@require_http_methods(["GET", "POST"])
def editar_usuario(request, id_usuario):
    from django.core.exceptions import ValidationError
    from django.core.validators import validate_email

    if request.session.get("rol") != "ADMINISTRADOR":
        return redirect("login")

    administrador = Usuario.objects.filter(
        id_usuario=request.session.get("id_usuario"),
        rol="ADMINISTRADOR"
    ).first()

    if not administrador:
        request.session.flush()
        return redirect("login")

    objetivo = Usuario.objects.filter(id_usuario=id_usuario).first()
    if not objetivo:
        return redirect("usuarios_funciones")

    contexto = {
        "objetivo": objetivo,
        "datos": {
            "nombre": objetivo.nombre,
            "correo": objetivo.correo,
            "telefono": objetivo.telefono,
            "direccion": objetivo.direccion,
        },
    }

    if request.method == "POST":
        datos = {
            "nombre": request.POST.get("nombre", "").strip(),
            "correo": request.POST.get("correo", "").strip().lower(),
            "telefono": request.POST.get("telefono", "").strip(),
            "direccion": request.POST.get("direccion", "").strip(),
        }
        contexto["datos"] = datos

        try:
            validate_email(datos["correo"])
            correo_valido = True
        except ValidationError:
            correo_valido = False

        error = None

        if not all(datos.values()):
            error = "Completa todos los campos."
        elif not correo_valido:
            error = "Ingresa un correo v\u00e1lido."
        elif (len(datos["nombre"]) > 100 or len(datos["correo"]) > 120
              or len(datos["telefono"]) > 20 or len(datos["direccion"]) > 150):
            error = "Alg\u00fan campo es demasiado largo."
        elif Usuario.objects.filter(
            correo__iexact=datos["correo"]
        ).exclude(id_usuario=objetivo.id_usuario).exists():
            error = "Ese correo ya lo usa otro usuario."

        if error:
            contexto["error"] = error
        else:
            objetivo.nombre = datos["nombre"]
            objetivo.correo = datos["correo"]
            objetivo.telefono = datos["telefono"]
            objetivo.direccion = datos["direccion"]
            objetivo.save(update_fields=["nombre", "correo", "telefono", "direccion"])

            if objetivo.id_usuario == administrador.id_usuario:
                request.session["nombre"] = objetivo.nombre

            contexto["exito"] = "Datos actualizados correctamente."

    return render(request, "core/editar_usuario.html", contexto)


def personalizar_interfaz(request):
    if request.session.get("rol") != "ADMINISTRADOR":
        return redirect("login")

    administrador = Usuario.objects.filter(
        id_usuario=request.session.get("id_usuario"),
        rol="ADMINISTRADOR"
    ).first()

    if not administrador:
        request.session.flush()
        return redirect("login")

    personalizados = dict(
        TextoInterfaz.objects.values_list("clave", "texto")
    )
    error = None

    if request.method == "POST":
        nuevos = {}

        for clave, defecto in ETIQUETAS_INTERFAZ.items():
            valor = request.POST.get(clave, "").strip()

            if not valor:
                error = "Todos los nombres deben tener texto."
                break

            if len(valor) > 100:
                error = "Los nombres no pueden superar 100 caracteres."
                break

            nuevos[clave] = valor

        if error:
            personalizados.update(nuevos)
        else:
            for clave, valor in nuevos.items():
                TextoInterfaz.objects.update_or_create(
                    clave=clave,
                    defaults={"texto": valor}
                )

            return redirect("/personalizar-interfaz/?guardado=1")

    campos = [
        {
            "clave": clave,
            "nombre": defecto,
            "texto": personalizados.get(clave, defecto),
        }
        for clave, defecto in ETIQUETAS_INTERFAZ.items()
    ]

    return render(request, "core/personalizar_interfaz.html", {
        "campos": campos,
        "error": error,
        "guardado": request.GET.get("guardado") == "1",
    })
