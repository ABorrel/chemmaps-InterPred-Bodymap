from django.conf.urls import url
from django.views.generic import TemplateView
from django.conf.urls.static import static
from django.conf import settings

from . import views

app_name = "toolchem"

urlpatterns = [
    url(
        r'^$',
        views.index,
        name='home'
    ),
] + static(settings.STATIC_URL, document_root="/home/sandbox/ChemMap2Site/static/toolchem/")

