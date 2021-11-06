# -*- coding: utf-8 -*-
try:
    import django
except ImportError:
    django = None

__version__ = '0.1.2'

if django and django.VERSION < (3, 2):  # pragma: no cover
    default_app_config = 'drf_pdf_renderer.apps.DjangoPdfRendererConfig'
