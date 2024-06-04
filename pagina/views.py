from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.hashers import make_password
from django.contrib.auth.hashers import check_password
from django.contrib.auth import authenticate, login 
from django.contrib.auth.decorators import login_required
from .models import Usuario, Propiedad, Imagen, Requisito
from django.core.files.base import ContentFile
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as autenticacion, logout
import json

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
        if User.objects.filter(email=correo).exists():
            message = 'El correo electrónico ya está registrado.'
            return render(request, 'registrarse.html', {'message': message})

        BaseUsuaruo = Usuario(
            nombre=nombre, 
            apellido=apellido,
            correo=correo,
            contrasena=make_password(contrasena), 
            rol=rol
        )
        
        BaseUsuaruo.save()
        
        is_superuser = 1 if BaseUsuaruo.rol == 'Arrendador' else 0
        
        # Crear un nuevo usuario
        usuario = User.objects.create_user(
            username=correo,
            email=correo,
            password=contrasena,
            first_name=nombre,
            last_name=apellido, 
            is_superuser=is_superuser,
        )
        usuario.save()

        # Autenticar al usuario
        user = authenticate(username=correo, password=contrasena)
        autenticacion(request, user)
        
        if user is not None:
            if BaseUsuaruo.rol == 'Arrendador':
                return redirect('/Alojamientos', usuario)
            else:
                return redirect('/Alojamientos')  # Redirigir a la página de publicar arrendatarios 
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

        # Autenticar el usuario en Django
        user = authenticate(request, username=usuario.correo, password=contrasena)
        if user is not None:
            autenticacion(request, user)
            request.session['usuario_id'] = usuario.id_usuario
            rolUser= usuario.rol
            if rolUser == 'Arrendador':
                return redirect('/Alojamientos', usuario)  # Redirigir a la página de inicio arrendador
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

        try:
            user = User.objects.get(username=usuario.correo)
            user.set_password(nueva_contrasena)
            user.save()
        except User.DoesNotExist:
            messages.error(request, 'No se encontró un usuario con ese correo electrónico.')
            return render(request, 'recuperar_contrasena.html')

        usuario.contrasena = make_password(nueva_contrasena)
        usuario.save()
        messages.success(request, 'La contraseña se ha cambiado correctamente.')
        return redirect('/IniciarSesion')
    
    return render(request, 'cambiarcontraseña.html')

def services(request):
    return render(request, 'servicios.html')

def condicionesuso(request):
    return render(request, 'condiciones_servicio.html')
#-----------------------------------------------------------
#VER LOS ALOJAMIENTOS -----------------------------------------------------------------------
#-----------------------------------------------------------

def ver_alojamientos(request):
    propiedades = Propiedad.objects.all().prefetch_related('imagenes')
    datos_propiedades = []

    for propiedad in propiedades:
        imagenes = []
        for imagen in propiedad.imagenes.all():
            try:
                if imagen.imagen:  # Verificar si hay un archivo asociado
                    imagen_url = imagen.imagen.url
                    direccion = imagen.imagen.url.split('?')
                    imagenes.append(direccion[0])
            except ValueError:
                # Manejar el caso en el que la imagen no tiene un archivo asociado
                pass
        print(imagenes)
        datos_propiedad = {
            'id_propiedad': propiedad.id_propiedad,
            'direccion': propiedad.direccion,
            'numero_contacto': propiedad.numero_contacto,
            'precio': propiedad.precio,
            'tipo_bano': propiedad.tipo_bano,
            'num_habitaciones': propiedad.num_habitaciones,
            'tipo_propiedad': propiedad.tipo_propiedad,
            'descripcion': propiedad.descripcion,
            'id_usuario': propiedad.id_usuario.id_usuario,  # Acceder a la clave primaria
            'nombre_barrio': propiedad.nombre_barrio,
            'servicios': propiedad.servicios,
            'requisitos': propiedad.requisitos,
            'imagenes': imagenes,
        }
        datos_propiedades.append(datos_propiedad)
    contexto = {'propiedades': datos_propiedades}
    print("hola")
    return render(request, 'ver_alojamientos.html', contexto)


#vista de alojamientos arrendador
def descripcion(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        print("hola", data.get("imagenes"))
        return render(request, 'descripcion.html', {'propiedad': data})
    else:
        # Renderizar la plantilla 'descripcion.html' sin datos si la solicitud no es POST
        return render(request, 'descripcion.html')

def publicaciones(request):
    return render(request,'publicar_alojamiento.html')
#-----------------------------------------------------------
# PUBLICAR -----------------------------------------------------------------------
#-----------------------------------------------------------
def publicar(request):
    print(request.user.username)
    user = User.objects.get(username=request.user.username)
    # Obtener el objeto Usuario asociado al usuario autenticado
    usuario = Usuario.objects.get(correo=user.email)

    if usuario.rol == 'Arrendador':
        if request.method == 'POST':
            # Obtener los datos del formulario
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

            propiedad = Propiedad.objects.create(
                direccion=direccion,
                numero_contacto=numero_contacto,
                precio=precio,
                tipo_bano=tipo_bano,
                num_habitaciones=num_habitaciones,
                tipo_propiedad=tipo_propiedad,
                descripcion=descripcion,
                id_usuario=usuario,  # Asignar la instancia de Usuario
                servicios=', '.join(servicios),
                nombre_barrio = barrio_nombre,
                requisitos=', '.join(requisitos)

            )

            # Guardar las imágenes
            imagenes = request.FILES.getlist('imagenes')
            for imagen in imagenes:
                img = Imagen(imagen=imagen, id_propiedad=propiedad)
                img.save()

            messages.success(request, 'La propiedad se ha publicado correctamente.')
            return redirect('/Alojamientos')

        return render(request, 'ver_alojamientos.html')
    else:
        messages.error(request, 'Debes iniciar sesión como Arrendador para publicar una propiedad.')
        return redirect('/IniciarSesion')
    
def logout_view(request):
    logout(request)
    return redirect('/')
