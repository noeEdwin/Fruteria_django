from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

# --- 1. MANAGER PERSONALIZADO (PARA EL LOGIN) ---
class EmpleadoManager(BaseUserManager):
    def create_user(self, username, password=None, nombre=None, id_e=None, turno=None, salario=None, **extra_fields):
        if not username or not password or not nombre or not id_e:
            raise ValueError('Faltan campos obligatorios')
        user = self.model(
            username=username,
            nombre=nombre,
            id_e=id_e,
            turno=turno,
            salario=salario,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password=None, nombre=None, id_e=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(username, password, nombre, id_e, **extra_fields)
# --- 2. MODELO EMPLEADO (TU MODELO DE USUARIO) ---
class Empleado(AbstractBaseUser, PermissionsMixin):
    
    id_e = models.IntegerField(primary_key=True)
    nombre = models.CharField(max_length=60, blank=True, null=True)
    TURNO_CHOICES = [
        ('Matutino', 'Matutino'),
        ('Vespertino', 'Vespertino'),
    ]
    turno = models.CharField(max_length=20, choices=TURNO_CHOICES, blank=True, null=True)
    salario = models.DecimalField(max_digits=14, decimal_places=2, blank=True, null=True)
    username = models.CharField(max_length=150, unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    
    # --- Conexiones ---
    objects = EmpleadoManager()

    # Campo que se usará para el login
    USERNAME_FIELD = 'username'
    # Campos que se pedirán al crear un superusuario (además de id_e, username, password)
    REQUIRED_FIELDS = ['nombre', 'id_e'] 

    def __str__(self):
        return self.username

    class Meta:
        managed = False      
        db_table = 'empleado' 


class Proveedor(models.Model):
    id_p = models.IntegerField(primary_key=True)
    nombre = models.CharField(max_length=80, blank=True, null=True)
    ciudad = models.CharField(max_length=30, blank=True, null=True)
    contacto = models.CharField(max_length=70, blank=True, null=True)
    tel_contacto = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        managed = False 
        db_table = 'proveedor'

    def __str__(self):
        return self.nombre

class Producto(models.Model):
    codigo = models.IntegerField(primary_key=True)
    descripcion = models.CharField(max_length=50, blank=True, null=True)
    categoria = models.CharField(max_length=50, blank=True, null=True)
    unidad_medida = models.CharField(max_length=20, blank=True, null=True)
    existencia = models.IntegerField(blank=True, null=True)
    precio_c = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    precio_v = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)

    class Meta:
        db_table = 'producto'
        managed = False

    def __str__(self):
        return f"{self.descripcion} ({self.codigo})"


class ProductoProveedor(models.Model):
    id = models.AutoField(primary_key=True) 
    codigo = models.ForeignKey(Producto, models.DO_NOTHING, db_column='codigo')
    id_p = models.ForeignKey(Proveedor, models.DO_NOTHING, db_column='id_p')

    class Meta:
        db_table = 'producto_proveedor'
        managed = False
        unique_together = (('codigo', 'id_p'),) 

class Cliente(models.Model):
    id_c = models.IntegerField(primary_key=True)
    telefono = models.CharField(max_length=12, blank=True, null=True)
    rfc = models.CharField(max_length=16, blank=True, null=True)
    domicilio = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        db_table = 'cliente'
        managed = False

    def __str__(self):
        return f"Cliente {self.id_c} ({self.rfc})"

class PMoral(models.Model):
    id_c = models.OneToOneField(Cliente, models.DO_NOTHING, db_column='id_c', primary_key=True)
    razon_social = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        db_table = 'p_moral'
        managed = False

    def __str__(self):
        return self.razon_social

class PFisica(models.Model):
    id_c = models.OneToOneField(Cliente, models.DO_NOTHING, db_column='id_c', primary_key=True)
    nombre = models.CharField(max_length=25, blank=True, null=True)

    class Meta:
        db_table = 'p_fisica'
        managed = False

    def __str__(self):
        return self.nombre

class Supervisor(models.Model):
    id = models.AutoField(primary_key=True) # PK "falso"
    id_e = models.ForeignKey(Empleado, models.DO_NOTHING, related_name='empleado_supervisado', db_column='id_e')
    id_s = models.ForeignKey(Empleado, models.DO_NOTHING, related_name='supervisor_a_cargo', db_column='id_s')

    class Meta:
        db_table = 'supervisor'
        managed = False
        unique_together = (('id_e', 'id_s'),)


class Venta(models.Model):
    folio_v = models.IntegerField(primary_key=True)
    fecha = models.DateField(blank=True, null=True)
    id_c = models.ForeignKey(Cliente, models.DO_NOTHING, db_column='id_c')
    id_e = models.ForeignKey(Empleado, models.DO_NOTHING, db_column='id_e')

    class Meta:
        db_table = 'venta'
        managed = False

    def __str__(self):
        return f"Venta {self.folio_v}"

class DetalleVenta(models.Model):
    id = models.AutoField(primary_key=True) # PK "falso"
    codigo = models.ForeignKey(Producto, models.DO_NOTHING, db_column='codigo')
    folio_v = models.ForeignKey(Venta, models.DO_NOTHING, db_column='folio_v')
    observaciones = models.CharField(max_length=50, blank=True, null=True)
    cantidad = models.IntegerField(blank=True, null=True)

    class Meta:
        db_table = 'detalle_venta'
        managed = False
        unique_together = (('codigo', 'folio_v'),)

class Compra(models.Model):
    folio_c = models.IntegerField(primary_key=True)
    no_lote = models.IntegerField(blank=True, null=True)
    fecha = models.DateField(blank=True, null=True)
    id_p = models.ForeignKey(Proveedor, models.DO_NOTHING, db_column='id_p')
    id_e = models.ForeignKey(Empleado, models.DO_NOTHING, db_column='id_e')

    class Meta:
        db_table = 'compra'
        managed = False

    def __str__(self):
        return f"Compra {self.folio_c}"

class DetalleCompra(models.Model):
    id = models.AutoField(primary_key=True) # PK "falso"
    folio_c = models.ForeignKey(Compra, models.DO_NOTHING, db_column='folio_c')
    codigo = models.ForeignKey(Producto, models.DO_NOTHING, db_column='codigo')
    cantidad = models.IntegerField(blank=True, null=True)

    class Meta:
        db_table = 'detalle_compra'
        managed = False
        unique_together = (('folio_c', 'codigo'),)