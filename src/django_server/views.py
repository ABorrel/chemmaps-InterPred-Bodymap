from django.shortcuts import render
from django.views.generic import TemplateView
from django.conf import settings



class Home(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cebs_enabled'] = 'cebs' in settings.INSTALLED_APPS
        return context

