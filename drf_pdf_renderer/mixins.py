from rest_framework.settings import api_settings

from drf_pdf_renderer.renderer import PDFRendererPaginated


class PdfAllResultsMixin:
    renderer_classes = (*api_settings.DEFAULT_RENDERER_CLASSES, PDFRendererPaginated)

    def paginate_queryset(self, queryset):
        if self.paginator and self.request.accepted_renderer.format == "pdf":
            self.paginator.page_size = 99999
        return super().paginate_queryset(queryset)
