from django.urls import path
from .views import (MangaLords, carrito, directorio, inicioSecion, pagar, Registro,
                    contacto, vistaManga, agregar_producto, listar_productos,
                    modificar_manga, eliminar_producto, admin, cerrarSesion,
                    request_password_reset, verify_reset_code, reset_password,
                    search_suggestions, perfil)

# imagenes
from django.conf import settings
from django.contrib.staticfiles.urls import static

urlpatterns = [
    path('',MangaLords, name='MangaLords'),
    path('carrito/',carrito, name='carrito'),
    path('administrador/', admin, name='admin'),
    path('directorio/',directorio, name="directorio"),
    path('inicioSecion/',inicioSecion, name='inicioSecion'),
    path('pagar/',pagar, name="pagar"),
    path('RegistroUsuario/',Registro, name='RegistroUsuario'),
    path('contacto/',contacto, name='contacto'),
    path('vistaManga/<str:pk>',vistaManga, name='vistaManga'),
    path('cerrarSesion/',cerrarSesion, name='cerrarSesion'),
    path('perfil/', perfil, name='perfil'),

    
    # Password reset OTP
    path('password-reset/request/', request_password_reset, name='request_password_reset'),
    path('password-reset/verify/', verify_reset_code, name='verify_reset_code'),
    path('password-reset/reset/', reset_password, name='reset_password'),
    
    # Autocomplete suggestions
    path('buscar-sugerencias/', search_suggestions, name='search_suggestions'),
    
    #crud
    path('agregar_producto/', agregar_producto, name="agregar_producto"),    
    path('listar_productos/', listar_productos, name="listar_productos"),     
    path('modificar_manga/<id>/', modificar_manga, name="modificar_manga"),     
    path('eliminar_producto/<id>/', eliminar_producto, name="eliminar_producto")
    
    #Carrito
    
    
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)