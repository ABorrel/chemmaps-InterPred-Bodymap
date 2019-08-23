from django.conf.urls import url
from django.views.generic import TemplateView

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
    ]