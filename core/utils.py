from django.conf import settings

def format_currency(amount):
    """
    Standardized currency formatter for GH₵.
    Can be easily updated if currency requirements change.
    """
    symbol = getattr(settings, 'CURRENCY_SYMBOL', 'GH₵')
    try:
        return f"{symbol}{float(amount):,.2f}"
    except (ValueError, TypeError):
        return f"{symbol}0.00"

def get_brand_info():
    """
    Centralized brand identity data.
    """
    return {
        'company_name': 'Sellux Plaster Ltd',
        'slogan': 'Home of Affordable Luxury',
        'address': 'Odokor, Dr. Busia Highway, Accra, Ghana',
        'phone_primary': '055 208 8784',
        'phone_secondary': '054 992 6773',
        'email': 'selluxplasterltd@gmail.com',
        'whatsapp': '233549926773',
    }
