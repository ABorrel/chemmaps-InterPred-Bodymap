from django.conf.urls import url
from django.views.generic import TemplateView
from django.conf.urls.static import static
from django.conf import settings

from . import views

app_name = "bodymap"

urlpatterns = [
    url(
        r'^$',
        views.index,
        name='home'
    ),
    url(
        r'^assaysMapping/$',
        views.mappingAssaysBody,
        name='assaysMapping'
    ),
    url(
        r'^assaysMappingTable/$',
        views.mappingAssaysBody,
        name='assaysMappingTable'

    ),
    url(
        r'^chemMapping/$',
        views.mappingChemicalToBody,
        name='chemMapping'
    ),
    url(
        r'^chemMappingTable/$',
        views.mappingChemicalToBody,
        name='chemMappingTable'

    ),
    ]+ static(settings.STATIC_URL, document_root="/home/sandbox/ChemMap2Site/static/bodymap/")

