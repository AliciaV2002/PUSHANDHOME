from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.hashers import make_password
from django.contrib.auth.hashers import check_password
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.decorators import login_required
from .models import Usuario, Propiedad, Imagen, Requisito
from django.core.files.base import ContentFile
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as autenticacion, logout

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

        # Crear un nuevo usuario
        usuario = User.objects.create_user(
            username=correo,
            email=correo,
            password=contrasena,
            first_name=nombre,
            last_name=apellido
        )
        usuario.save()

        BaseUsuaruo = Usuario(
            nombre=nombre, 
            apellido=apellido,
            correo=correo,
            contrasena=make_password(contrasena), 
            rol=rol)
        
        BaseUsuaruo.save()
        # Autenticar al usuario
        user = authenticate(username=correo, password=contrasena)
        if user is not None:
            autenticacion(request, user)
            if BaseUsuaruo.rol == 'Arrendador':
                return redirect('/Publicar_alojamientos', usuario_id=BaseUsuaruo.id_usuario)
            else:
                return redirect('/Alojamientos', usuario_id=BaseUsuaruo.id_usuario)

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
#-----------------------------------------------------------
#VER LOS ALOJAMIENTOS -----------------------------------------------------------------------
#-----------------------------------------------------------
def ver_alojamientos(request):
    propiedades = Propiedad.objects.all()
    contexto = {'propiedades': propiedades}
    return render(request, 'ver_alojamientos.html', contexto)

#vista de alojamientos arrendador
def alojamientos_pub(request):
    propiedades = Propiedad.objects.all()
    contexto = {'propiedades': propiedades}
    return render(request, 'alojamientos_publicados.html',contexto)

def descripcion(request):
    # Obtener el índice de la propiedad de la URL
    index = request.GET.get('index')
    if index is not None:
        try:
            # Convertir el índice a entero
            index = int(index)
            # Obtener todas las propiedades
            propiedades = Propiedad.objects.all()
            # Verificar si el índice está dentro del rango de las propiedades
            if 0 <= index < len(propiedades):
                # Obtener la propiedad correspondiente al índice
                propiedad = propiedades[index]
                # Pasar la propiedad a la plantilla
                return render(request, 'descripcion.html', {'propiedad': propiedad})
        except (ValueError, Propiedad.DoesNotExist):
            pass
    # Si el índice no es válido o no se proporciona, redirigir a una página de error o a la página principal
    return render(request, 'error.html')  # O renderizar una página de error

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
                requisitos=requisitos
            )

            # Guardar las imágenes
            imagenes = request.FILES.getlist('imagenes')
            for imagen in imagenes:
                img = Imagen(imagen=imagen, id_propiedad=propiedad)
                img.save()

            messages.success(request, 'La propiedad se ha publicado correctamente.')
            return redirect('/Alojamientos')

        return render(request, 'alojamientos_publicados.html')
    else:
        messages.error(request, 'Debes iniciar sesión como Arrendador para publicar una propiedad.')
        return redirect('/IniciarSesion')