import re

from django.http import HttpResponse
from django.template.loader import render_to_string
from rest_framework.renderers import BaseRenderer
from xhtml2pdf import pisa

from drf_pdf_renderer.utils import link_callback


class MountPdfMixin:

    def get_template(self):
        if hasattr(self.context['view'], 'pdf_get_renderer_template'):
            return self.context['view'].pdf_get_renderer_template(self.data)
        elif hasattr(self.context['view'], 'pdf_renderer_template'):
            return self.context['view'].pdf_renderer_template
        return 'pdf/list_portrait.html'

    def mount_show_fields(self):
        if hasattr(self.context['view'], 'pdf_get_display_fields'):
            return self.context['view'].pdf_get_display_fields(self.data)
        elif hasattr(self.context['view'], 'pdf_display_fields'):
            return self.context['view'].pdf_display_fields

        return []

    def get_title(self):
        if hasattr(self.context['view'], 'pdf_get_title'):
            return self.context['view'].pdf_get_title(self.data)
        elif hasattr(self.context['view'], 'pdf_title'):
            return self.context['view'].pdf_title

        return re.sub(r"(\w)([A-Z])", r"\1 \2", self.context['view'].__class__.__name__)

    def mount_context(self):
        base_context = {
            'data': self.data, 
            'request': self.context['request'],
            **self.get_additional_context()
        }

        if hasattr(self.context['view'], 'pdf_mount_context'):
            return {
                **self.context['view'].pdf_mount_context(self.data),
                **base_context
            }

        return base_context

    def get_additional_context(self):
        return {
            'fields': self.mount_show_fields(),
            'title': self.get_title()
        }

    def render_template(self):
        return render_to_string(template_name=self.get_template(), context=self.mount_context())

    @staticmethod
    def render_pdf(template):
        return pisa.CreatePDF(template, link_callback=link_callback).dest


class PDFRenderer(MountPdfMixin, BaseRenderer):
    media_type = 'application/pdf'
    format = 'pdf'

    def get_pdf_filename(self, pdf):
        if hasattr(self.context['view'], 'pdf_get_filename'):
            return self.context['view'].pdf_get_filename(pdf, self.data)
        elif hasattr(self.context['view'], 'pdf_filename'):
            return self.context['view'].pdf_filename

        return 'report.pdf'

    def mount_response(self, pdf):
        filename = self.get_pdf_filename(pdf)
        response = HttpResponse(pdf.getvalue(), content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename={filename}'
        return response

    def process_render(self):
        if self.data is None or self.context['response'].status_code >= 300:
            return self.data

        template = self.render_template()
        pdf = self.render_pdf(template)
        return self.mount_response(pdf)

    def render(self, data, accepted_media_type=None, renderer_context=None):
        self.data = data
        self.context = renderer_context
        return self.process_render()


class PDFRendererPaginated(PDFRenderer):
    results_field = 'results'

    def render(self, data, *args, **kwargs):
        if not isinstance(data, list):
            data = data.get(self.results_field, [])
        return super().render(data, *args, **kwargs)
