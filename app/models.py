from typing import Any, Dict, Tuple
from django.db import models
# from django.contrib.auth.hashers import make_password
# filtro para la barnav
from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User



# Create your models here. // usar pal carrito igual
class Manga(models.Model):
    id = models.CharField(primary_key=True,max_length=6, verbose_name ="Id") #llave primaria
    titulo = models.CharField(max_length=50, verbose_name ="Título")
    imagen = models.ImageField(upload_to='imagenes/', verbose_name ="Imagenes" ,null=True)
    editorial = models.CharField(max_length=50, verbose_name ="Editotial")
    precio = models.IntegerField(verbose_name ="Precio")
    descripcion = models.TextField(max_length=1000, verbose_name ="Descripción")
    cantidad = models.IntegerField(verbose_name ="Cantidad")
    descuento = models.IntegerField(default=0, verbose_name="Descuento (%)")

    def __str__(self):
        fila = "Título: "+ self.titulo
        return fila
    
    #borrar registro de img del admin  y acá
    def delete(self, using=None, keep_parent=False):
        self.imagen.storage.delete(self.imagen.name)
        super().delete()


# registarse modod formulario de django
def validar_no_vacio(value):
    if not value:
        raise ValidationError('Este campo no puede estar vacío.')

class RegistroUsuario(models.Model):
    user = models.OneToOneField( User, on_delete=models.CASCADE, primary_key=True )
    USERNAME_FIELD = 'username'
    nombres = models.CharField(max_length=500, validators=[validar_no_vacio])
    apellidos = models.CharField(max_length=500, validators=[validar_no_vacio])
    telefono = models.IntegerField(validators=[validar_no_vacio])
    email = models.EmailField(validators=[validar_no_vacio])
    
    def __str__(self):
        return self.nombres
    

# Contacto

opc_consulta = [
        [0,"Reclamos"],
        [1,"Sugerencias"],
        [2,"Consultas"],
        [3,"Problemas con mi pedido"]
    ]
    
class Contacto(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='contactos')
    nombre = models.CharField(max_length=50)
    email = models.EmailField()
    telefono = models.IntegerField()
    tipo_consulta = models.IntegerField(choices=opc_consulta)
    mensaje = models.TextField()
    respuesta = models.TextField(null=True, blank=True, verbose_name="Respuesta del Administrador")
    respondido = models.BooleanField(default=False, verbose_name="Respondido")
    fecha_creacion = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Consulta", null=True, blank=True)
    fecha_respuesta = models.DateTimeField(null=True, blank=True, verbose_name="Fecha de Respuesta")
    # avisos = models.BooleanField("Recibir Avisos", default=True)
    
    def __str__(self):
        return f"{self.nombre} - {self.get_tipo_consulta_display()}"
    
    #recuerda revisar el admin y agregar el contacto


class Pedido(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='pedidos')
    transaction_id = models.CharField(max_length=50, unique=True, verbose_name="ID de Transacción")
    nombre = models.CharField(max_length=200, verbose_name="Nombre Completo")
    email = models.EmailField(verbose_name="Email")
    telefono = models.CharField(max_length=20, verbose_name="Teléfono")
    direccion = models.CharField(max_length=500, verbose_name="Dirección")
    total_price = models.IntegerField(verbose_name="Total Pagado")
    fecha = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Compra")
    tarjeta_ultimos_cuatro = models.CharField(max_length=4, verbose_name="Últimos 4 dígitos")

    def __str__(self):
        return f"Pedido {self.transaction_id} - {self.user.username}"


class DetallePedido(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE, related_name='detalles')
    manga_titulo = models.CharField(max_length=100, verbose_name="Título del Manga")
    manga_editorial = models.CharField(max_length=100, verbose_name="Editorial")
    precio_unitario = models.IntegerField(verbose_name="Precio Unitario")
    cantidad = models.IntegerField(verbose_name="Cantidad")
    subtotal = models.IntegerField(verbose_name="Subtotal")
    manga = models.ForeignKey(Manga, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.manga_titulo} x {self.cantidad}"


class Notificacion(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notificaciones')
    mensaje = models.CharField(max_length=500)
    leido = models.BooleanField(default=False)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.mensaje} - {'Leída' if self.leido else 'No leída'}"


