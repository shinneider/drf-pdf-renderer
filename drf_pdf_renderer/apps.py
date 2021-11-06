# -*- coding: utf-8 -*-
from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class DjangoPdfRendererConfig(AppConfig):  # Our app config class
    name = 'drf_pdf_renderer'
    verbose_name = _('Django PDF Renderer')
