from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static
from . import views
from django.conf import settings


urlpatterns = [
    path('', views.index),	
    path('Registrarse/', views.register),
    path('IniciarSesion/', views.login),
    path('CerrarSesion/', views.logout_view),  # Nueva URL para cerrar sesión
    path('CambiarContraseña/', views.changepass),
    path('NuestrosServicios/', views.services),
    path('CondicionesdeUso/', views.condicionesuso),
    path('Alojamientos/', views.ver_alojamientos),
    path('Descripcion_de_alojamientos/', views.descripcion),
    #nueva -> modificaron html alojamientos, funcion de alojamientos_pub, modificacion en register y login.
    path('Registro_publicacion/', views.publicaciones),
    path('Publicar_alojamientos/', views.publicar),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
