from django.db import models

class Usuario(models.Model):
    id_usuario = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50)
    correo = models.EmailField(unique=True)
    contrasena = models.CharField(max_length=100)
    rol = models.CharField(max_length=20, choices=[('Arrendador', 'Arrendador'), ('Arrendatario', 'Arrendatario')])

    def __str__(self):
        return f"{self.nombre} {self.apellido}"

class Barrio(models.Model):
    id_barrio = models.AutoField(primary_key=True)
    nombre_barrio = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.nombre_barrio

class Propiedad(models.Model):
    id_propiedad = models.AutoField(primary_key=True)
    direccion = models.CharField(max_length=200)
    numero_contacto = models.CharField(max_length=20)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    tipo_bano = models.CharField(max_length=20, choices=[('Privado', 'Privado'), ('Compartido', 'Compartido')])
    num_habitaciones = models.IntegerField()
    tipo_propiedad = models.CharField(max_length=20, choices=[('Casa', 'Casa'), ('Apartamento', 'Apartamento'), ('Habitacion', 'Habitacion')])
    descripcion = models.TextField(blank=True, null=True)
    id_usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    id_barrio = models.ForeignKey(Barrio, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.direccion}, {self.id_barrio.nombre_barrio}"

class Imagen(models.Model):
    id_imagen = models.AutoField(primary_key=True)
    imagen = models.BinaryField()
    id_propiedad = models.ForeignKey(Propiedad, on_delete=models.CASCADE)

    def __str__(self):
        return f"Imagen {self.id_imagen}"