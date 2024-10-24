from django.urls import re_path as url
from django.views.generic import TemplateView
from django.conf import settings
from . import views

handler404 = "chemmaps.views.handler404"
handler500 = "chemmaps.views.handler500"
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


    ### help pages ###
    ##################
    url(
        r'^DrugMap3D/DrugMapHelp',
        views.launchHelp,
        {"map":"drugbank"},
        name='DrugMapHelp'
    ),

    url(
        r'^DSSToxMap3D/DSSToxMapHelp',
        views.launchHelp,
        {"map": "DSSToxMapHelp"},
        name='DSSTOXMapHelp'
    ),

    url(
        r'^Tox21MapHelp/$',
        views.launchHelp,
        {"map": "Tox21MapHelp"},
        name='Tox21MapHelp'
    ),

    ### DrugMap ###
    ###############
    url(
        r'^DrugMap/$',
        views.launchMap,
        {"map":"drugbank"},
        name='DrugMap',
    ),
    url(
        r'^DrugMap3D/$',
        views.launchMap,
        {"map":"drugbank"},
        name='DrugMap3D'
    ),

    url(
        r'^DrugMapSmilesUploaded/$',
        views.launchMap,
        {"map":"drugbank"},
        name='DrugMapSMILES'
    ),
    url(
        r'^DrugMapDescriptors/$',
        views.computeDescriptor,
        {"map":"drugbank"},
        name='DrugMapDescriptors'
    ),
    url(
        r'^DrugMapAdd/$',
        views.computeDescriptor,
        {"map": "drugbank"},
        name='DrugMapAdd'
    ),


    # DSSToxMap
    url(
        r'^DSSToxMap/$',
        views.launchMap,
        {"map":"dsstox"},
        name='DSSToxMap',
    ),
    url(
        r'^DSSToxMap3D/$',
        views.launchMap,
        {"map":"dsstox"},
        name='DSSToxMap3D'
    ),

    url(
        r'^DSSToxMapSmilesUploaded/$',
        views.launchMap,
        {"map":"dsstox"},
        name='DSSToxMapSMILES'
    ),
    url(
        r'^DSSToxMapDescriptors/$',
        views.computeDescriptor,
        {"map":"dsstox"},
        name='DSSToxMapDescriptors'
    ),
    url(
        r'^DSSToxMapAdd/$',
        views.computeDescriptor,
        {"map": "dsstox"},
        name='DSSToxMapAdd'
    ),

    #Tox21Map
    url(
        r'^Tox21Map/$',
        views.launchMap,
        {"map":"tox21"},
        name='Tox21Map',
    ),
    url(
        r'^Tox21Map3D/$',
        views.launchMap,
        {"map":"tox21"},
        name='Tox21Map3D'
    ),

    url(
        r'^Tox21MapSmilesUploaded/$',
        views.launchMap,
        {"map":"tox21"},
        name='Tox21MapSMILES'
    ),
    url(
        r'^Tox21MapDescriptors/$',
        views.computeDescriptor,
        {"map":"tox21"},
        name='Tox21MapDescriptors'
    ),
    url(
        r'^Tox21MapAdd/$',
        views.computeDescriptor,
        {"map": "tox21"},
        name='Tox21MapAdd'
    ),


    # PFAS
    url(
        r'^PFASMap/$',
        views.launchMap,
        {"map":"pfas"},
        name='PFASMap',
    ),
    url(
        r'^PFASMap3D/$',
        views.launchMap,
        {"map":"pfas"},
        name='PFASMap3D'
    ),
    url(
        r'^PFASMap3D/PFASMapHelp',
        views.launchHelp,
        {"map": "pfas"},
        name='PFASMapHelp'
    ),
    url(
        r'^PFASMapSmilesUploaded/$',
        views.launchMap,
        {"map": "pfas"},
        name='PFASMapSMILES'
    ),
    url(
        r'^PFASMapDescriptors/$',
        views.computeDescriptor,
        {"map": "pfas"},
        name='PFASMapDescriptors'
    ),
    url(
        r'^PFASMapAdd/$',
        views.computeDescriptor,
        {"map": "pfas"},
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
        r'.*DSSTox/(?P<DTXSID>[-\w]+)$', views.launchDSSToxMap, name="DSSToxSp",
    ),
    url(
        r'^tox21/target=(?P<target>[-\w]+)', views.launchTox21TagetMap, name="Tox21Target",
    ),
    url(
        r'^tox21/mostactive', views.launchTox21MostPotent, name="Tox21MostPotent",
    ),
    url(
        r'^tox21/browsechemicals', views.browseChemicals, name="browseChemicals",
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
    ),
    url(
        r'^lowestAC50.csv',
        views.download, {"name": "lowestAC50"}, name="lowestAC50",
    )
]
