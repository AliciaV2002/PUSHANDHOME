from django.contrib import admin
from django.urls import path
from . import views
urlpatterns = [
    path('', views.index),	
    path('registrarse/', views.register),
    path('iniciarsesion/', views.login),
    path('cambiarcontraseña/', views.changepass)
]
