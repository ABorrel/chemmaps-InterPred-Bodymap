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
        r'uploadChem',
        views.upload_chem,
        name='upload_chem'
    ),

    url(
        r'computeDesc',
        views.compute_desc,
        name='compute_desc'
    ),
    url(
        r'computeOPERA',
        views.compute_opera,
        name='compute_opera'
    ),
    url(
        r'computeInterPred',
        views.compute_interference,
        name='compute_interference'
    ),

    url(
        r'^chemicals.csv',
        views.download, {"name": "chemicals"}, name="chemical",
    ),


] + static(settings.STATIC_URL, document_root=settings.PROJECT_PATH)

