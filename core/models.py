from django.db import models


class ReglaConversion(models.Model):
    id_regla = models.AutoField(primary_key=True)
    puntos_por_kg = models.DecimalField(max_digits=6, decimal_places=2)
    vigente_desde = models.DateField()
    activa = models.BooleanField(default=True)

    def __str__(self):
        return f"Regla {self.id_regla}: {self.puntos_por_kg} puntos/kg"


class Usuario(models.Model):
    ROL_CHOICES = [
    ("GENERADOR", "Generador"),
    ("RECOLECTOR", "Recolector"),
    ("ADMINISTRADOR", "Administrador"),
    ("SIN_ROL", "Sin rol"),
]
    id_usuario = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    correo = models.CharField(max_length=120, unique=True)
    contrasena_hash = models.CharField(max_length=255)
    telefono = models.CharField(max_length=20)
    direccion = models.CharField(max_length=150)
    rol = models.CharField(max_length=20, choices=ROL_CHOICES)

    def __str__(self):
        return f"{self.nombre} ({self.rol})"


class Solicitud(models.Model):
    ESTADO_CHOICES = [
        ("PENDIENTE", "Pendiente"),
        ("ASIGNADA", "Asignada"),
        ("RECOLECTADA", "Recolectada"),
        ("CANCELADA", "Cancelada"),
    ]

    id_solicitud = models.AutoField(primary_key=True)
    generador = models.ForeignKey(
        Usuario, on_delete=models.PROTECT, db_column="id_generador"
    )
    direccion = models.CharField(max_length=150)
    peso_estimado = models.DecimalField(max_digits=8, decimal_places=2)
    tipo_material = models.CharField(
        max_length=20,
        choices=[
            ("PLASTICO", "Pl?stico"),
            ("PAPEL", "Papel"),
            ("CARTON", "Cart?n"),
            ("VIDRIO", "Vidrio"),
            ("METAL", "Metal"),
            ("OTROS", "Otros"),
        ],
        default="OTROS",
    )
    franja_horaria = models.CharField(max_length=30)
    codigo_qr = models.CharField(max_length=64, unique=True)
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES)
    fecha_solicitud = models.DateTimeField()

    def __str__(self):
        return f"Solicitud {self.id_solicitud} - {self.estado}"


class Recoleccion(models.Model):
    id_recoleccion = models.AutoField(primary_key=True)
    solicitud = models.OneToOneField(
        Solicitud, on_delete=models.PROTECT, db_column="id_solicitud"
    )
    recolector = models.ForeignKey(
        Usuario, on_delete=models.PROTECT, db_column="id_recolector"
    )
    peso_real = models.DecimalField(max_digits=8, decimal_places=2)
    fecha_hora = models.DateTimeField()

    def __str__(self):
        return f"Recolección {self.id_recoleccion}"


class Recibo(models.Model):
    id_recibo = models.AutoField(primary_key=True)
    usuario = models.ForeignKey(
        Usuario, on_delete=models.PROTECT, db_column="id_usuario"
    )
    periodo = models.CharField(max_length=7)
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    descuento_aplicado = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Recibo {self.id_recibo} - {self.periodo}"


class MovimientoPuntos(models.Model):
    TIPO_CHOICES = [
        ("ACUMULA", "Acumula"),
        ("REDIME", "Redime"),
    ]

    id_movimiento = models.AutoField(primary_key=True)
    usuario = models.ForeignKey(
        Usuario, on_delete=models.PROTECT, db_column="id_usuario"
    )
    recoleccion = models.OneToOneField(
        Recoleccion,
        on_delete=models.PROTECT,
        db_column="id_recoleccion",
        null=True,
        blank=True,
    )
    recibo = models.ForeignKey(
        Recibo,
        on_delete=models.PROTECT,
        db_column="id_recibo",
        null=True,
        blank=True,
    )
    regla = models.ForeignKey(
        ReglaConversion,
        on_delete=models.PROTECT,
        db_column="id_regla",
        null=True,
        blank=True,
    )
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES)
    cantidad = models.IntegerField()
    fecha = models.DateTimeField()

    def __str__(self):
        return f"Movimiento {self.id_movimiento} - {self.tipo} {self.cantidad}"


class Ruta(models.Model):
    id_ruta = models.AutoField(primary_key=True)
    recolector = models.ForeignKey(
        Usuario, on_delete=models.PROTECT, db_column="id_recolector"
    )
    fecha = models.DateField()

    def __str__(self):
        return f"Ruta {self.id_ruta} - {self.fecha}"


class RutaParada(models.Model):
    id_parada = models.AutoField(primary_key=True)
    ruta = models.ForeignKey(
        Ruta, on_delete=models.PROTECT, db_column="id_ruta"
    )
    solicitud = models.OneToOneField(
        Solicitud, on_delete=models.PROTECT, db_column="id_solicitud"
    )
    orden = models.IntegerField()

    def __str__(self):
        return f"Parada {self.orden} de la ruta {self.ruta_id}"


class PermisoUsuario(models.Model):
    FUNCION_CHOICES = [
        ("ADMIN_USUARIOS", "Administrar usuarios"),
        ("ADMIN_SOLICITUDES", "Administrar solicitudes"),
        ("SOLICITAR_RECOLECCION", "Solicitar recolecci\u00f3n"),
        ("REGISTRAR_RECOLECCIONES", "Registrar recolecciones"),
    ]

    id_permiso = models.AutoField(primary_key=True)
    usuario = models.ForeignKey(
        Usuario,
        on_delete=models.CASCADE,
        db_column="id_usuario",
        related_name="permisos_extra",
    )
    funcion = models.CharField(max_length=40, choices=FUNCION_CHOICES)

    class Meta:
        unique_together = ("usuario", "funcion")

    def __str__(self):
        return f"{self.usuario_id} - {self.funcion}"
