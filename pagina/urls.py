from django.contrib import admin
from django.urls import path
from . import views


urlpatterns = [
    path('', views.index),	
    path('Registrarse/', views.register),
    path('IniciarSesion/', views.login),
    path('CambiarContraseña/', views.changepass),
    path('NuestrosServicios/', views.services),
    path('CondicionesdeUso/', views.condicionesuso),
    path('Alojamientos/', views.ver_alojamientos),
    path('Publicaciones/', views.alojamientos_pub),
    path('Descripcion_de_alojamientos/', views.descripcion),
    path('Publicar_alojamientos/', views.publicar),
]
