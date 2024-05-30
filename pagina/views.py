from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages

# Create your views here.
def index(request):
    return render(request, 'index.html')

def register(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        apellido = request.POST.get('apellido')
        correo = request.POST.get('correo')
        contrasena = request.POST.get('contrasena')
        rol = request.POST.get('rol')

        # Verificar si el correo ya está registrado
        if Usuario.objects.filter(correo=correo).exists():
            messages.error(request, 'El correo electrónico ya está registrado. Por favor, ingresa uno diferente.')
            # return render(request, 'registrarse.html')
        else:
        # Crear un nuevo usuario
            usuario = Usuario(nombre=nombre, apellido=apellido, correo=correo, contrasena=contrasena, rol=rol)
            usuario.save()

        # Redirigir a otra página después del registro exitoso
            messages.success(request, 'Registro exitoso. ¡Bienvenido a Push & Home!')
            return redirect('/Alojamientos')

    return render(request, 'registrarse.html')

def login(request):
    return render(request, 'iniciarsesion.html')

def changepass(request):
    return render(request, 'cambiarcontraseña.html')

def services(request):
    return render(request, 'servicios.html')

def condicionesuso(request):
    return render(request, 'condiciones_servicio.html')

def ver_alojamientos(request):
    return render(request, 'ver_alojamientos.html')

def alojamientos_pub(request):
    return render(request, 'alojamientos_publicados.html')






from .models import Usuario
from django.shortcuts import render, redirect

def registrar_usuario(request):
    
    return render(request, 'registro.html')