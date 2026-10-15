
import random
import uuid
from datetime import date, timedelta
from decimal import Decimal

from django.contrib.auth.hashers import make_password
from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils import timezone

from core.models import (
    MovimientoPuntos,
    Recibo,
    Recoleccion,
    ReglaConversion,
    Ruta,
    RutaParada,
    Solicitud,
    Usuario,
)

NOMBRES = [
    "Ana", "Luis", "Maria", "Carlos", "Laura",
    "Jorge", "Sofia", "Andres", "Valentina", "Camilo",
    "Daniela", "Felipe", "Paula", "Sebastian",
    "Camila", "Juan", "Isabella", "David", "Mariana",
    "Santiago",
]

APELLIDOS = [
    "Gomez", "Rodriguez", "Martinez", "Lopez", "Garcia",
    "Perez", "Sanchez", "Ramirez", "Torres", "Diaz",
    "Vargas", "Castro", "Ortiz", "Rojas", "Moreno",
    "Jimenez", "Herrera", "Medina", "Silva", "Cruz",
]

BARRIOS = [
    "Centro", "Los Almendros", "El Prado", "San Jose",
    "La Floresta", "Villa Nueva", "El Carmen", "Las Palmas",
]

FRANJAS = [
    "08:00 - 10:00",
    "10:00 - 12:00",
    "14:00 - 16:00",
    "16:00 - 18:00",
]


def decimal(minimo, maximo):
    return Decimal(str(round(random.uniform(minimo, maximo), 2)))


class Command(BaseCommand):
    help = "Carga datos de prueba para EcoRutaBio"

    def add_arguments(self, parser):
        parser.add_argument(
            "--limpiar",
            action="store_true",
            help="Borra los datos actuales antes de cargar",
        )

    @transaction.atomic
    def handle(self, *args, **options):

        if options["limpiar"]:
            for modelo in (
                MovimientoPuntos,
                RutaParada,
                Recoleccion,
                Recibo,
                Ruta,
                Solicitud,
                Usuario,
                ReglaConversion,
            ):
                modelo.objects.all().delete()

        elif any(modelo.objects.exists() for modelo in (ReglaConversion, Solicitud, Recoleccion, Recibo, MovimientoPuntos, Ruta, RutaParada)):
            self.stdout.write(
                self.style.WARNING(
                    "Ya hay datos. Usa --limpiar para reemplazarlos."
                )
            )
            return

        random.seed(42)
        ahora = timezone.now()
        clave = make_password("Clave12345")

        # Crear 100 reglas de conversion
        reglas = []

        for i in range(100):
            regla = ReglaConversion.objects.create(
                puntos_por_kg=decimal(5, 20),
                vigente_desde=date(2024, 1, 1)
                + timedelta(days=7 * i),
                activa=(i == 99),
            )
            reglas.append(regla)

        regla_activa = reglas[-1]

        # Crear 100 usuarios
        generadores = []
        recolectores = []

        for i in range(100):

            if i < 60:
                rol = "GENERADOR"
            elif i < 90:
                rol = "RECOLECTOR"
            else:
                rol = "ADMINISTRADOR"

            usuario = Usuario.objects.create(
                nombre=(
                    f"{random.choice(NOMBRES)} "
                    f"{random.choice(APELLIDOS)}"
                ),
                correo=f"usuario{i + 1}@ecorutabio.test",
                contrasena_hash=clave,
                telefono=f"300{random.randint(1000000, 9999999)}",
                direccion=(
                    f"Calle {random.randint(1, 120)} # "
                    f"{random.randint(1, 90)}-"
                    f"{random.randint(1, 99)}, "
                    f"{random.choice(BARRIOS)}"
                ),
                rol=rol,
            )

            if rol == "GENERADOR":
                generadores.append(usuario)
            elif rol == "RECOLECTOR":
                recolectores.append(usuario)

        # Crear 120 solicitudes con diferentes estados
        estados = (
            ["RECOLECTADA"] * 100
            + ["PENDIENTE"] * 8
            + ["ASIGNADA"] * 8
            + ["CANCELADA"] * 4
        )

        solicitudes = []

        for i, estado in enumerate(estados):
            generador = random.choice(generadores)

            solicitud = Solicitud.objects.create(
                generador=generador,
                direccion=generador.direccion,
                peso_estimado=decimal(1, 50),
                franja_horaria=random.choice(FRANJAS),
                codigo_qr=(
                    f"QR-{i + 1:06d}-"
                    f"{uuid.uuid4().hex[:16]}"
                ),
                estado=estado,
                fecha_solicitud=ahora - timedelta(
                    days=random.randint(3, 120),
                    hours=random.randint(0, 23),
                ),
            )

            solicitudes.append(solicitud)

        recolectadas = solicitudes[:100]

        # Crear 100 recolecciones
        recolecciones = []

        for solicitud in recolectadas:
            factor = Decimal(
                str(round(random.uniform(0.9, 1.1), 2))
            )

            peso = max(
                Decimal("0.50"),
                (
                    solicitud.peso_estimado * factor
                ).quantize(Decimal("0.01")),
            )

            recoleccion = Recoleccion.objects.create(
                solicitud=solicitud,
                recolector=random.choice(recolectores),
                peso_real=peso,
                fecha_hora=(
                    solicitud.fecha_solicitud
                    + timedelta(hours=random.randint(2, 48))
                ),
            )

            recolecciones.append(recoleccion)

        # Crear 100 rutas y sus respectivas paradas
        for solicitud, recoleccion in zip(
            recolectadas, recolecciones
        ):
            ruta = Ruta.objects.create(
                recolector=recoleccion.recolector,
                fecha=recoleccion.fecha_hora.date(),
            )

            RutaParada.objects.create(
                ruta=ruta,
                solicitud=solicitud,
                orden=1,
            )

        # Crear 100 recibos
        recibos = []

        for _ in range(100):
            valor = decimal(20000, 150000)

            descuento = (
                valor
                * Decimal(
                    str(round(random.uniform(0.02, 0.25), 2))
                )
            ).quantize(Decimal("0.01"))

            fecha = ahora - timedelta(
                days=30 * random.randint(0, 11)
            )

            recibo = Recibo.objects.create(
                usuario=random.choice(generadores),
                periodo=fecha.strftime("%Y-%m"),
                valor=valor,
                descuento_aplicado=descuento,
            )

            recibos.append(recibo)

        # Crear 100 movimientos que acumulan puntos
        for recoleccion in recolecciones:
            MovimientoPuntos.objects.create(
                usuario=recoleccion.solicitud.generador,
                recoleccion=recoleccion,
                regla=regla_activa,
                tipo="ACUMULA",
                cantidad=int(
                    recoleccion.peso_real
                    * regla_activa.puntos_por_kg
                ),
                fecha=recoleccion.fecha_hora,
            )

        # Crear 20 movimientos que redimen puntos
        for recibo in recibos[:20]:
            MovimientoPuntos.objects.create(
                usuario=recibo.usuario,
                recibo=recibo,
                tipo="REDIME",
                cantidad=random.randint(50, 500),
                fecha=ahora - timedelta(
                    days=random.randint(0, 60)
                ),
            )

        self.stdout.write(self.style.SUCCESS("Datos cargados:"))

        for modelo in (
            ReglaConversion,
            Usuario,
            Solicitud,
            Recoleccion,
            Recibo,
            MovimientoPuntos,
            Ruta,
            RutaParada,
        ):
            self.stdout.write(
                f"  {modelo.__name__}: {modelo.objects.count()}"
            )

