from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.hashers import make_password
from django.contrib.auth.hashers import check_password
from django.contrib.auth import authenticate, login as auth_login
from .models import Usuario

# Create your views here.
def index(request):
    return render(request, 'index.html')
#-----------------------------------------------------------
# REGISTRARSE -----------------------------------------------------------------------
#-----------------------------------------------------------
def register(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        apellido = request.POST.get('apellido')
        correo = request.POST.get('correo')
        contrasena = request.POST.get('contrasena')
        rol = request.POST.get('rol')

        # Verificar si el correo ya está registrado
        if Usuario.objects.filter(correo=correo).exists():
            message = 'El correo electrónico ya está registrado.'
            return render(request, 'registrarse.html', {'message': message})
        
        # Crear un nuevo usuario
        usuario = Usuario(nombre=nombre, apellido=apellido, correo=correo, contrasena=make_password(contrasena), rol=rol)
        usuario.save()

    # Redirigir a otra página después del registro exitoso
        messages.success(request, 'Registro exitoso. ¡Bienvenido a Push & Home!')
        return redirect('/Alojamientos')

    return render(request, 'registrarse.html')
#-----------------------------------------------------------
# INICIAR SESIÓN -----------------------------------------------------------------------
#-----------------------------------------------------------
def login(request):
    if request.method == 'POST':
        correo = request.POST.get('correo')
        contrasena = request.POST.get('contrasena')

        try:
            usuario = Usuario.objects.get(correo=correo)
        except Usuario.DoesNotExist:
            messages.error(request, 'Credenciales inválidas.')
            return render(request, 'iniciarsesion.html')

        if check_password(contrasena, usuario.contrasena):
            # Iniciar sesión
            request.session['usuario_id'] = usuario.id_usuario
            messages.success(request, 'Inicio de sesión exitoso.')
            return redirect('/Alojamientos')  # Redirigir a la página de inicio
        else:
            messages.error(request, 'Credenciales inválidas.')

    return render(request, 'iniciarsesion.html')
#-----------------------------------------------------------
#RECUPERAR CONTRASEÑA -----------------------------------------------------------------------
#-----------------------------------------------------------
def changepass(request):
    if request.method == 'POST':
        correo = request.POST.get('correo')
        nueva_contrasena = request.POST.get('nueva_contrasena')

        try:
            usuario = Usuario.objects.get(correo=correo)
        except Usuario.DoesNotExist:
            messages.error(request, 'No se encontró un usuario con ese correo electrónico.')
            return render(request, 'recuperar_contrasena.html')

        usuario.contrasena = make_password(nueva_contrasena)
        usuario.save()
        messages.success(request, 'La contraseña se ha cambiado correctamente.')
        return redirect('/CambiarContraseña')
    
    return render(request, 'cambiarcontraseña.html')

def services(request):
    return render(request, 'servicios.html')

def condicionesuso(request):
    return render(request, 'condiciones_servicio.html')

def ver_alojamientos(request):
    return render(request, 'ver_alojamientos.html')

def alojamientos_pub(request):
    return render(request, 'alojamientos_publicados.html')

def descripcion(request):
    return render(request, 'descripcion.html')

def publicar(request):
    return render(request, 'publicar_arrendador.html')