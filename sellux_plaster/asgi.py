"""ASGI config for sellux_plaster project.

It exposes the ASGI callable as a module-level variable named ``application``.
"""
import os
from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sellux_plaster.settings')

application = get_asgi_application()
