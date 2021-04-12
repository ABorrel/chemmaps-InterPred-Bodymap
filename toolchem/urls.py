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
        r'checkDesc',
        views.checkAlreadyComputedDesc,
        name='check_already_computed'
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
        r'computeCoords',
        views.compute_coords,
        name='compute_coords'
    ),
    url(
        r'uploadDataFiles',
        views.upload_datafiles,
        name='upload_datafiles'
    ),
    url(
        r'uploadAssayFile',
        views.upload_assayfile,
        name='upload_assayfile'
    ),
    url(
        r'^pushUpdate',
        views.pushUpdate, 
        name="pushUpdate",
    ),
    url(
        r'^push',
        views.push, 
        name="push",
    ),
    
    url(
        r'^clearuserchem',
        views.clearuserchem, 
        name="clearuser",
    ),
       
    url(
        r'^chemicals.csv',
        views.download, {"name": "chemicals"}, name="chemical",
    ),
    

] + static(settings.STATIC_URL, document_root=settings.PROJECT_PATH)

