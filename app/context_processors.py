from .models import Notificacion

def cart_counter(request):
    total_items = 0
    if 'cart' in request.session:
        try:
            cart = request.session['cart']
            if isinstance(cart, dict):
                total_items = sum(int(q) for q in cart.values())
        except (ValueError, TypeError):
            total_items = 0
    return {
        'cart_total_items': total_items
    }

def notifications_processor(request):
    if request.user.is_authenticated:
        # Traer notificaciones ordenadas por fecha (más recientes primero)
        notifs = Notificacion.objects.filter(user=request.user).order_by('-fecha_creacion')
        unread_count = notifs.filter(leido=False).count()
        return {
            'header_notifications': notifs[:15],  # Mostrar las últimas 15 en el panel
            'unread_notifications_count': unread_count
        }
    return {
        'header_notifications': [],
        'unread_notifications_count': 0
    }
