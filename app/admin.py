from django.contrib import admin
from .models import Manga, RegistroUsuario, Contacto, Pedido, DetallePedido

# Register your models here.
class Homeadmin(admin.ModelAdmin):
    list_display =["titulo", "precio","cantidad"]
    list_editable = ["precio"]
    search_fields = ["titulo", "editorial"]

def obtener_opciones_filtro():
    opciones = Manga.objects.values_list('titulo', flat=True).distinct()
    return [(opcion, opcion) for opcion in opciones]
    

class DetallePedidoInline(admin.TabularInline):
    model = DetallePedido
    extra = 0
    readonly_fields = ["manga_titulo", "manga_editorial", "precio_unitario", "cantidad", "subtotal", "manga"]

class PedidoAdmin(admin.ModelAdmin):
    list_display = ["transaction_id", "user", "nombre", "total_price", "fecha", "tarjeta_ultimos_cuatro"]
    search_fields = ["transaction_id", "nombre", "user__username"]
    list_filter = ["fecha"]
    inlines = [DetallePedidoInline]
    readonly_fields = ["user", "transaction_id", "nombre", "email", "telefono", "direccion", "total_price", "fecha", "tarjeta_ultimos_cuatro"]

admin.site.register(Manga, Homeadmin)
admin.site.register(RegistroUsuario)
admin.site.register(Contacto)
admin.site.register(Pedido, PedidoAdmin)
admin.site.register(DetallePedido)




