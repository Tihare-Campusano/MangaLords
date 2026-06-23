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
