from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.hashers import make_password
from django.contrib.auth.hashers import check_password
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.decorators import login_required
from .models import Usuario, Barrio, Propiedad, Imagen
from django.core.files.base import ContentFile

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
            rolUser= usuario.rol

            if rolUser == 'Arrendador':
                return redirect('/Publicaciones', usuario)  # Redirigir a la página de inicio arrendador
            else:
                return redirect('/Alojamientos')  # Redirigir a la página de publicar arrendatarios 
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
    
    return render(request, 'iniciarsesion.html')

def services(request):
    return render(request, 'servicios.html')

def condicionesuso(request):
    return render(request, 'condiciones_servicio.html')

def ver_alojamientos(request):
    return render(request, 'ver_alojamientos.html')

#vista de alojamientos arrendador
def alojamientos_pub(request):
    return render(request, 'alojamientos_publicados.html')

def descripcion(request):
    return render(request, 'descripcion.html')



def publicar(request):
    if request.method == 'POST':
        
        if not request.user.is_authenticated:
            messages.error(request, 'Debes iniciar sesión para publicar una propiedad.')
            return redirect('login')
        if request.user.is_authenticated:
            # Obtener el usuario actual
            usuario = request.user.usuario

            direccion = request.POST.get('direccion')
            barrio_nombre = request.POST.get('barrio')
            numero_contacto = request.POST.get('numero_contacto')
            precio = request.POST.get('precio')
            tipo_bano = request.POST.get('tipo_bano')
            num_habitaciones = request.POST.get('num_habitaciones')
            tipo_propiedad = request.POST.get('tipo_propiedad')
            descripcion = request.POST.get('descripcion')
            servicios = request.POST.getlist('servicios')
            requisitos = request.POST.getlist('requisitos')

            # Obtener o crear el objeto Barrio
            barrio, _ = Barrio.objects.get_or_create(nombre_barrio=barrio_nombre)

            # Crear el objeto Propiedad
            propiedad = Propiedad(
                direccion=direccion,
                numero_contacto=numero_contacto,
                precio=precio,
                tipo_bano=tipo_bano,
                num_habitaciones=num_habitaciones,
                tipo_propiedad=tipo_propiedad,
                descripcion=descripcion,
                id_usuario=usuario,
                id_barrio=barrio,
                servicios=', '.join(servicios),
                requisitos=', '.join(requisitos)
            )
            propiedad.save()

            # Guardar las imágenes
            imagenes = request.FILES.getlist('imagenes')
            for imagen in imagenes:
                img = Imagen(imagen=ContentFile(imagen.read()), id_propiedad=propiedad)
                img.save()

            messages.success(request, 'La propiedad se ha publicado correctamente.')
        
        else:
            messages.error(request, 'Debes iniciar sesión para publicar una propiedad.')
            return redirect('/IniciarSesion')

    return render(request, 'publicar_alojamiento.html')
