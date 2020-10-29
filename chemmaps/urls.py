from django.conf.urls import url
from django.views.generic import TemplateView
from django.conf.urls.static import static
from django.conf import settings

from . import views

app_name = "chemmaps"

urlpatterns = [
    url(
        r'^$',
        views.index,
        name='home'
    ),
    url(
        r'^help$',
        views.launchHelp,
        name='help'
    ),


    ### DrugMap ###
    ###############
    url(
        r'^DrugMap/$',
        views.launchMap,
        {"map":"DrugMap"},
        name='DrugMap',
    ),
    url(
        r'^DrugMap3D/$',
        views.launchMap,
        {"map":"DrugMap"},
        name='DrugMap3D'
    ),
    url(
        r'^DrugMap3D/DrugMapHelp',
        views.launchHelp,
        {"map":"DrugMap"},
        name='DrugMapHelp'
    ),
    url(
        r'^DrugMapSmilesUploaded/$',
        views.launchMap,
        {"map":"DrugMap"},
        name='DrugMapSMILES'
    ),
    url(
        r'^DrugMapDescriptors/$',
        views.computeDescriptor,
        {"map":"DrugMap"},
        name='DrugMapDescriptors'
    ),
    url(
        r'^DrugMapAdd/$',
        views.computeDescriptor,
        {"map": "DrugMap"},
        name='DrugMapAdd'
    ),


    # DSSToxMap
    url(
        r'^DSSToxMap/$',
        views.launchMap,
        {"map":"DSSToxMap"},
        name='DSSToxMap',
    ),
    url(
        r'^DSSToxMap3D/$',
        views.launchMap,
        {"map":"DSSToxMap"},
        name='DSSToxMap3D'
    ),
    url(
        r'^DSSToxMap3D/DSSToxMapHelp',
        views.launchHelp,
        {"map": "DSSToxMapHelp"},
        name='helpMap'
    ),
    url(
        r'^DSSToxMapSmilesUploaded/$',
        views.launchMap,
        {"map":"DSSToxMap"},
        name='DSSToxMapSMILES'
    ),
    url(
        r'^DSSToxMapDescriptors/$',
        views.computeDescriptor,
        {"map":"DSSToxMap"},
        name='DSSToxMapDescriptors'
    ),
    url(
        r'^DSSToxMapAdd/$',
        views.computeDescriptor,
        {"map": "DSSToxMap"},
        name='DSSToxMapAdd'
    ),

    #Tox21Map
    url(
        r'^Tox21Map/$',
        views.launchMap,
        {"map":"Tox21Map"},
        name='Tox21Map',
    ),
    url(
        r'^Tox21Map3D/$',
        views.launchMap,
        {"map":"Tox21Map"},
        name='Tox21Map3D'
    ),
    url(
        r'Tox21MapHelp$',
        views.launchHelp,
        {"map": "Tox21MapHelp"},
        name='helpMap'
    ),
    url(
        r'^Tox21MapSmilesUploaded/$',
        views.launchMap,
        {"map":"Tox21Map"},
        name='Tox21MapSMILES'
    ),
    url(
        r'^Tox21MapDescriptors/$',
        views.computeDescriptor,
        {"map":"Tox21Map"},
        name='Tox21MapDescriptors'
    ),
    url(
        r'^Tox21MapAdd/$',
        views.computeDescriptor,
        {"map": "Tox21Map"},
        name='Tox21MapAdd'
    ),


    # PFAS
    url(
        r'^PFASMap/$',
        views.launchMap,
        {"map":"PFASMap"},
        name='PFASMap',
    ),
    url(
        r'^PFASMap3D/$',
        views.launchMap,
        {"map":"PFASMap"},
        name='PFASMap3D'
    ),
    url(
        r'^PFASMap3D/PFASMapHelp',
        views.launchHelp,
        {"map": "PFASMap"},
        name='PFASMapHelp'
    ),
    url(
        r'^PFASMapSmilesUploaded/$',
        views.launchMap,
        {"map": "PFASMap"},
        name='PFASMapSMILES'
    ),
    url(
        r'^PFASMapDescriptors/$',
        views.computeDescriptor,
        {"map": "PFASMap"},
        name='PFASMapDescriptors'
    ),
    url(
        r'^PFASMapAdd/$',
        views.computeDescriptor,
        {"map": "PFASMap"},
        name='PFASMapAdd'
    ),

    # Other page
    #url(
    #    r'^uploadChem/$',
    #    views.UploadChem, name='uploadChem'
    #),
    #url(
    #    r'^smilesprocess/$',
    #    views.DrugMap, name="smilesprocess",
    #),
    url(
        r'^descriptor/$',
        views.computeDescriptor, name="descriptor",
    ),

    url(
        r'DSSTox/(?P<DTXSID>[-\w]+)', views.launchDSSToxMap, name="DSSToxSp",
    ),
    url(
        r'^tox21/(?P<assay>[-\w]+)', views.launchTox21AssayMap, name="Tox21Sp",
    ),
    url(
        r'^2D.csv',
        views.download, {"name": "2D"}, name="2D",

    ),
    url(
        r'^3D.csv',
        views.download, {"name": "3D"}, name="3D",

    )


] + static(settings.STATIC_URL, document_root="/home/sandbox/ChemMap2Site/static/chemmaps/")

