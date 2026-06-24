from django.urls import path
from .views import (MangaLords, carrito, directorio, inicioSecion, pagar, Registro,
                    contacto, vistaManga, agregar_producto, listar_productos,
                    modificar_manga, eliminar_producto, admin, cerrarSesion,
                    request_password_reset, verify_reset_code, reset_password,
                    search_suggestions, perfil, export_mangas_excel, export_mangas_pdf,
                    export_users_excel, export_users_pdf, download_manga_template,
                    agregar_al_carrito, eliminar_del_carrito, actualizar_cantidad_carrito,
                    pago_exitoso, compras_realizadas, toggle_user_role, responder_contacto,
                    get_notifications, mark_notification_read, mark_all_notifications_read)

# imagenes
from django.conf import settings
from django.contrib.staticfiles.urls import static

urlpatterns = [
    path('',MangaLords, name='MangaLords'),
    path('carrito/',carrito, name='carrito'),
    path('carrito/agregar/<str:pk>/', agregar_al_carrito, name='agregar_al_carrito'),
    path('carrito/eliminar/<str:pk>/', eliminar_del_carrito, name='eliminar_del_carrito'),
    path('carrito/actualizar/<str:pk>/', actualizar_cantidad_carrito, name='actualizar_cantidad_carrito'),
    path('pago_exitoso/', pago_exitoso, name='pago_exitoso'),
    path('compras/', compras_realizadas, name='compras_realizadas'),
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
    path('eliminar_producto/<id>/', eliminar_producto, name="eliminar_producto"),
    
    # exportaciones y plantillas de administracion
    path('administrador/exportar/mangas/excel/', export_mangas_excel, name="export_mangas_excel"),
    path('administrador/exportar/mangas/pdf/', export_mangas_pdf, name="export_mangas_pdf"),
    path('administrador/exportar/usuarios/excel/', export_users_excel, name="export_users_excel"),
    path('administrador/exportar/usuarios/pdf/', export_users_pdf, name="export_users_pdf"),
    path('administrador/plantilla-excel/', download_manga_template, name="download_manga_template"),
    path('administrador/usuario/cambiar-rol/<str:username>/', toggle_user_role, name='toggle_user_role'),
    path('administrador/mensajes/responder/<int:pk>/', responder_contacto, name='responder_contacto'),
    
    # Notificaciones API
    path('notificaciones/', get_notifications, name='get_notifications'),
    path('notificaciones/leer/<int:pk>/', mark_notification_read, name='mark_notification_read'),
    path('notificaciones/leer-todas/', mark_all_notifications_read, name='mark_all_notifications_read'),
    
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
