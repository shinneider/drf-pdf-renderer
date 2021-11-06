DRF PDF Renderer
=
A simplistic/very extendable pdf renderer.

If you use or like the project, click `Star` and `Watch` to generate metrics and i evaluate project continuity.

OBS
= 
This project is a `Beta` version, however is used in production in a big project (with custom pdf template, and manually fields instead of automatic).  
however, due to my low availability, updates may take some time.
but i will keep an eye on the PR.

# Install:
    pip install drf-pdf-renderer

# Usage:
1. Add to your `INSTALLED_APPS`, in `settings.py`:
    ```
    INSTALLED_APPS = [  
        ...
        'drf_pdf_renderer',
        ...
    ]
    ```

1. In your file:
    ```
    from rest_framework.settings import api_settings
    from drf_pdf_renderer.renderer import PDFRendererPaginated

    class YourView(...)
        renderer_classes = (*api_settings.DEFAULT_RENDERER_CLASSES, PDFRendererPaginated)
        pdf_display_fields = (['id', 'Label for ID'], )  # used only in automatic field (caution: refactor planned in futures versions)
        pdf_display_fields = ''  # contains two built-in templates ['pdf/list_landscape.html', 'pdf/list_portrait.html']
        ...
    ...

1. Mixin for paginated results
    - if you have a pagination on DRF, but require a PDF with all registries, you can use this Mixin

    ```
    from rest_framework.settings import api_settings
    from drf_pdf_renderer.mixin import PdfAllResultsMixin

    class YourView(PdfAllResultsMixin, ...)
        pdf_display_fields = (['id', 'Label for ID'], )  # used only in automatic field (caution: refactor planned in futures versions)
        pdf_display_fields = ''  # contains two built-in templates ['pdf/list_landscape.html', 'pdf/list_portrait.html']
        ...
    ...

# Advanced
1. Custom PDF Template
    - this project use [xhtml2pdf](https://github.com/xhtml2pdf/xhtml2pdf), check documentation of html constructor [here](https://xhtml2pdf.readthedocs.io/en/latest/format_html.html).
    
1. Changing PDF title
    ```
    # First way
    class YourView(...)
        pdf_title = 'My Title'
    
    # Second way
    class YourView(...)
        def pdf_get_title(self, data, context)
            return ''
    ```

1. Changing PDF download name
    ```
    # First way
    class YourView(...)
        pdf_filename = 'My Title'
    
    # Second way
    class YourView(...)
        def pdf_get_filename(self, pdf, data)
            return ''
    ```

1. Custom data to render context
    ```
    - By default `data`, `request`, `title` and `fields` will always be present (but can be rewrited)
    # Second way
    class YourView(...)
        def pdf_mount_context(data)
            return {'adm': True}
    ```