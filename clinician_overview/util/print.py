from django.http import HttpResponse
from django.template.loader import render_to_string
from xhtml2pdf import pisa
import os
from django.conf import settings
from django.contrib.staticfiles import finders

def link_callback(uri, rel):
    if uri.startswith(settings.MEDIA_URL):
        return os.path.join(settings.MEDIA_ROOT, uri.removeprefix(settings.MEDIA_URL))
    if uri.startswith(settings.STATIC_URL):
        path = finders.find(uri.removeprefix(settings.STATIC_URL))
        if path:
            return path
    return uri

def render_to_pdf(request, template_name, context, filename="document.pdf"):
    html = render_to_string(template_name, context, request=request)
    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = f'attachment; filename="{filename}"'
    result = pisa.CreatePDF(html, dest=response, link_callback=link_callback)
    if result.err:
        return HttpResponse("Error generating PDF", status=500)
    return response