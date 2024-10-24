"""django_server URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls import include
from .views import Home
from django.conf.urls.static import static
from django.urls import re_path as url

urlpatterns = [
    path('', Home.as_view(), name='home'),
    url(r'^chemmaps/', include(('chemmaps.urls', 'chemmaps'), namespace='chemmaps')),
    url(r'^interferences/', include(('interferences.urls', 'interferences'), namespace='interferences')),
    url(r'^bodymap/', include(('bodymap.urls', 'bodymap'), namespace='bodymap')),
    url(r'^toolchem/', include(('toolchem.urls', 'toolchem'), namespace='toolchem')),
]
