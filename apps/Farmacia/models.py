from django.db import models
from django.contrib.auth.models import AbstractUser


class Rol(models.Model):
    '''Roles Manejados por el sistema: Estos roles seran los que utilizara el sistema para todos aquellos que no sean
    administradores del sistema informatico (superuser)'''
    ADMIN = 1
    VENDEDOR = 2
    ROL_CHOICES = (
        (ADMIN, 'Administrador'),
        (VENDEDOR, 'Vendedor'),
        )

    id_rol = models.PositiveSmallIntegerField(choices=ROL_CHOICES, primary_key=True)

    class Meta:
        db_table = 'ROL'
    def __str__(self):
        return self.get_id_rol_display()

class User(AbstractUser):
    id_rol = models.ForeignKey(Rol, models.PROTECT, db_column='ID_ROL', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        db_table = 'USER'

    def __str__(self):
        return self.username

#---------------------------------------------------------------------------------------------------------------


class Presentacion(models.Model):
    id_presentacion = models.AutoField(db_column='ID_PRESENTACION', primary_key=True)  # Field name made lowercase.
    presentacion = models.TextField(db_column='PRESENTACION', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        db_table = 'PRESENTACION'
        ordering = ['id_presentacion'] # Para que funcione el paginado aplicar un orden por defecto

    def __str__(self):
        return self.presentacion

class TipoMedicamento(models.Model):
    id_tipo = models.AutoField(db_column='ID_TIPO', primary_key=True)  # Field name made lowercase.
    tipo = models.TextField(db_column='TIPO')  # Field name made lowercase.


    class Meta:
        db_table = 'TIPO_MEDICAMENTO'
        ordering = ['id_tipo'] # Para que funcione el paginado aplicar un orden por defecto

    def __str__(self):
        return self.tipo

class Medicamento(models.Model):
    id_medicamento = models.AutoField(db_column='ID_MEDICAMENTO', primary_key=True)  # Field name made lowercase.
    id_presentacion = models.ForeignKey('Presentacion', models.PROTECT, db_column='ID_PRESENTACION')  # Field name made lowercase.
    id_tipo = models.ForeignKey('TipoMedicamento', models.PROTECT, db_column='ID_TIPO')  # Field name made lowercase.
    nombre = models.TextField(db_column='NOMBRE')  # Field name made lowercase.
    precio = models.FloatField(db_column='PRECIO', default=0)  # Field name made lowercase.

    class Meta:
        db_table = 'MEDICAMENTO'
        ordering = ['id_medicamento'] # Para que funcione el paginado aplicar un orden por defecto

    def __str__(self):
        return self.nombre

#---------------------------------------------------------------------------------------------------------------
class Venta(models.Model):
    id_venta = models.AutoField(db_column='ID_VENTA', primary_key=True)  # Field name made lowercase.
    nombre_cliente = models.TextField(db_column='NOMBRE')  # Field name made lowercase.
    id_medicamento = models.ForeignKey(Medicamento, models.PROTECT, db_column='ID_MEDICAMENTO', blank=True, null=True)  # Field name made lowercase.
    cantidad = models.IntegerField(db_column='CANTIDAD', blank=True, null=True)  # Field name made lowercase.
    precio_neto = models.FloatField(db_column='PRECIO_NETO', blank=True, null=True)  # Field name made lowercase.
    fecha = models.DateField(db_column='FECHA')  # Field name made lowercase.
    total = models.FloatField(db_column='TOTAL')  # Field name made lowercase.

    class Meta:
        db_table = 'VENTA'
