from django.contrib import admin
from .models import Usuario, Propiedad, Imagen, Requisito

# Registra tus modelos aquí.
admin.site.register(Usuario)
admin.site.register(Propiedad)
admin.site.register(Imagen)
admin.site.register(Requisito)

# Agregar requisitos predeterminados si no existen
REQUISITOS_OPCIONES = [
    'No fumar',
    'Mayores de 18',
    'No tener mascotas',
    'Certificado de estudios',
    'Persona sola',
    'Solo mujeres',
    'Solo hombres',
    'No hacer fiestas',
    'No modificaciones a los enceres',
    'No hacer ruidos fuertes',
]

for nombre in REQUISITOS_OPCIONES:
    Requisito.objects.get_or_create(nombre=nombre)
