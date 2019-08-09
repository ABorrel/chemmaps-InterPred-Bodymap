from django.conf.urls import url
from django.views.generic import TemplateView

from . import views

app_name = "interferences"

urlpatterns = [
    url(r'^$',
        views.index,
        name='home'),
    url(
        r'^uploadSMILES/$',
        views.uploadSMILES,
        name='uploadSMILES',
    ),
    url(
        r'^cleanSMILES/$',
        views.uploadSMILES,
        name='cleanSMILES',
    ),
    url(
        r'^computeDESC/$',
        views.computeDesc,
        name='computeDESC',
    ),
    url(
        r'^results/$',
        views.computeDesc,
        name='results',
    ),
    url(
        r'^2D.csv',
        views.download, {"name": "2D"}, name="2D",
    ),
    url(
        r'^OPERA.csv',
        views.download, {"name": "OPERA"}, name="OPERA",
    ),
    url(
        r'^predict.csv',
        views.download, {"name": "predict"}, name="predict",
    ),
    url(
        r'^resources/$',
        views.resources,
        name='resources'
    ),
    ]

