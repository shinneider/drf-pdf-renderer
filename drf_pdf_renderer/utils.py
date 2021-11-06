import os

from django.conf import settings
from django.db.models.fields.related import ForeignKey


def link_callback(uri, rel):
    """
    Convert HTML URIs to absolute system paths so xhtml2pdf can access those
    resources
    """
    base_path = settings.BASE_DIR
    result, exists = f"{base_path}{uri}", os.path.exists(f"{base_path}{uri}")

    if exists:
        if not isinstance(result, (list, tuple)):
            result = [result]
        result = list(os.path.realpath(path) for path in result)
        path = result[0]
    else:
        static_url = settings.STATIC_URL        # Typically /static/
        static_root = settings.STATIC_ROOT      # Typically /home/userX/project_static/
        media_url = settings.MEDIA_URL         # Typically /media/
        media_root = settings.MEDIA_ROOT       # Typically /home/userX/project_static/media/

        if uri.startswith(media_url):
            path = os.path.join(media_root, uri.replace(media_url, ""))
        elif uri.startswith(static_url):
            path = os.path.join(static_root, uri.replace(static_url, ""))
        else:
            return uri

    # make sure that file exists
    if not os.path.isfile(path):
        raise Exception('media URI must start with %s or %s' % (static_url, media_url))
    return path
