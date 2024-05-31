from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def index(request):
    return render(request, 'index.html')

def register(request):
    return render(request, 'registrarse.html')

def login(request):
    return render(request, 'iniciarsesion.html')

def changepass(request):
    return render(request, 'cambiarcontraseña.html')

def services(request):
    return render(request, 'servicios.html')

def condicionesuso(request):
    return render(request, 'condiciones_servicio.html')

def alojamientos(request):
    return render(request, 'ver_alojamientos.html')

def descripcion(request):
    return render(request, 'descripcion.html')

def publicar(request):
    return render(request, 'publicar_arrendador.html')