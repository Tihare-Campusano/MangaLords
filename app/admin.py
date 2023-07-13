from django.contrib import admin
from .models import Manga,RegistroUsuario, Contacto

# Register your models here.
class Homeadmin(admin.ModelAdmin):
    list_display =["titulo", "precio","cantidad"]
    list_editable = ["precio"]
    search_fields = ["titulo", "editorial"]

def obtener_opciones_filtro():
    opciones = Manga.objects.values_list('titulo', flat=True).distinct()
    return [(opcion, opcion) for opcion in opciones]
    

admin.site.register(Manga, Homeadmin)
admin.site.register(RegistroUsuario)
admin.site.register(Contacto)

