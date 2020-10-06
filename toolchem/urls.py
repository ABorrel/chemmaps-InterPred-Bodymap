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

    url(
        r'testform',
        views.testForm,
        name='testform'
    ),

    url(
        r'uploadChem',
        views.uploadChem,
        name='uploadChem'
    ),

] + static(settings.STATIC_URL, document_root="/home/sandbox/ChemMap2Site/static/toolchem/")

