from django.urls import path
from .views import MangaLords, carrito, directorio, inicioSecion, pagar, Registro, contacto, vistaManga,agregar_producto, listar_productos, modificar_manga, eliminar_producto, admin, cerrarSesion

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
    
    #crud
    path('agregar_producto/', agregar_producto, name="agregar_producto"),    
    path('listar_productos/', listar_productos, name="listar_productos"),     
    path('modificar_manga/<id>/', modificar_manga, name="modificar_manga"),     
    path('eliminar_producto/<id>/', eliminar_producto, name="eliminar_producto")
    
    #Carrito
    
    
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)