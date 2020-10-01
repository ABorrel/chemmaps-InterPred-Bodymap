from django.shortcuts import render
from django.views.generic import TemplateView


# Create your views here.
def index(request):

    # update information from the DB

    return render(request, 'toolchem/index.html', {})