from django.db import models

# Create your models here.
class Proveedor(models.Model):
    # SQL: id_p INTEGER PRIMARY KEY
    id_p = models.IntegerField(primary_key=True)
    
    # SQL: nombre VARCHAR(80)
    nombre = models.CharField(max_length=80)
    
    # SQL: ciudad VARCHAR(30)
    ciudad = models.CharField(max_length=30)
    
    # SQL: contacto VARCHAR(70)
    contacto = models.CharField(max_length=70)
    
    # SQL: tel_contacto VARCHAR(20)
    tel_contacto = models.CharField(max_length=20)

    class Meta:
        db_table = 'proveedor'

    def __str__(self):
        return self.nombre