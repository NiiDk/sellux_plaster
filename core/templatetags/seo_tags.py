import json
from django import template
from django.utils.safestring import mark_safe

register = template.Library()

@register.simple_tag
def generate_business_schema(brand):
    """
    Generates LocalBusiness schema for SEO.
    """
    schema = {
        "@context": "https://schema.org",
        "@type": "LocalBusiness",
        "name": brand['company_name'],
        "description": brand['slogan'],
        "url": "https://sellux-plaster.onrender.com",
        "telephone": brand['phone_primary'],
        "address": {
            "@type": "PostalAddress",
            "streetAddress": "Odokor, Dr. Busia Highway",
            "addressLocality": "Accra",
            "addressCountry": "GH"
        },
        "geo": {
            "@type": "GeoCoordinates",
            "latitude": "5.5800",
            "longitude": "-0.2500"
        },
        "openingHoursSpecification": {
            "@type": "OpeningHoursSpecification",
            "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"],
            "opens": "08:00",
            "closes": "17:00"
        }
    }
    return mark_safe(f'<script type="application/ld+json">{json.dumps(schema)}</script>')

@register.simple_tag
def generate_product_schema(product):
    """
    Generates Product schema for e-commerce items.
    """
    schema = {
        "@context": "https://schema.org/",
        "@type": "Product",
        "name": product.name,
        "image": product.image.url if product.image else "",
        "description": product.description,
        "offers": {
            "@type": "Offer",
            "url": f"https://sellux-plaster.onrender.com{product.get_absolute_url()}",
            "priceCurrency": "GHS",
            "price": str(product.price),
            "availability": "https://schema.org/InStock" if product.stock > 0 else "https://schema.org/OutOfStock"
        }
    }
    return mark_safe(f'<script type="application/ld+json">{json.dumps(schema)}</script>')
