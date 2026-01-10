from .utils import get_brand_info
from cart.cart import Cart
from promotions.models import Promotion

def brand_context(request):
    """
    Exposes brand information globally to all templates.
    Use in templates as: {{ brand.company_name }}
    """
    return {
        'brand': get_brand_info()
    }

def cart_context(request):
    """
    Exposes the cart object to all templates.
    """
    return {'cart': Cart(request)}

def promotions_context(request):
    """
    Exposes the active promotion to all templates.
    """
    promotion = Promotion.objects.filter(is_active=True).first()
    return {'active_promotion': promotion}
