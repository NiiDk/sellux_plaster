"""WSGI config for sellux_plaster project.

It exposes the WSGI callable as a module-level variable named ``application``.
"""
import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sellux_plaster.settings')

application = get_wsgi_application()
