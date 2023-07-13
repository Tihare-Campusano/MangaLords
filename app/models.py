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
    nombre = models.CharField(max_length=50)
    email = models.EmailField()
    telefono = models.IntegerField()
    tipo_consulta = models.IntegerField(choices=opc_consulta)
    mensaje = models.TextField()
    # avisos = models.BooleanField("Recibir Avisos", default=True)
    
    def __str__(self):
        return self.nombre
    
    #recuerda revisar el admin y agregar el contacto
