from .utils import get_brand_info

def brand_context(request):
    """
    Exposes brand information globally to all templates.
    Use in templates as: {{ brand.company_name }}
    """
    return {
        'brand': get_brand_info()
    }
