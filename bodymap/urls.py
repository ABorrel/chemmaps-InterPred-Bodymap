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
        r'^help$',
        views.help,
        name='help'
    ),
    url(
        r'^chemMapping/$',
        views.mappingChemicalToBody,
        name='chemMapping'
    ),
    url(
        r'^chemMappingNameResult/$',
        views.mappingChemicalToBody,
        name='chemMapping'
    ),
    url(
        r'^bychem/(?P<CAS>[-\w]+)', 
        views.mappingChemicalToBodyByCASRN, 
        name="byCASRN"
    ),

    ] 

